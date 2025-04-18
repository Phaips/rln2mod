#!/usr/bin/env python3
import sys
import os
import subprocess
import argparse
import glob
import starfile
import warnings

# Suppress FutureWarnings from pandas and starfile
warnings.simplefilter('ignore', FutureWarning)

def process_star_files(x_dim, y_dim, z_dim):
    mod_dir = 'mod'
    os.makedirs(mod_dir, exist_ok=True)

    # Search for STAR files with strict and loose patterns
    patterns = ['*_particles.star', '*.star']
    all_matches = []
    for pat in patterns:
        matches = glob.glob(pat)
        if matches:
            print(f"Found {len(matches)} files matching {pat}: {matches}")
            all_matches.extend(matches)

    if not all_matches:
        print("No .star files found in this directory. Make sure you're in the right working directory and your files end in '.star' (or '_particles.star').")
        return

    for star_file in sorted(set(all_matches)):
        print(f"Processing: {star_file}")
        # Read STAR data (pick first block if multiple), suppressing warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', FutureWarning)
            data = starfile.read(star_file)
        df = data[next(iter(data))] if isinstance(data, dict) else data

        # Compute converted coordinates
        px = df['rlnTomoTiltSeriesPixelSize']
        xs = df['rlnCenteredCoordinateXAngst'] / px + x_dim / 2
        ys = df['rlnCenteredCoordinateYAngst'] / px + y_dim / 2
        zs = df['rlnCenteredCoordinateZAngst'] / px + z_dim / 2

        # Write to .txt
        base = os.path.splitext(star_file)[0]
        txt_file = f"{base}.txt"
        print(f"→ Writing intermediate coordinate file: {txt_file}")
        with open(txt_file, 'w') as out:
            for x, y, z in zip(xs, ys, zs):
                out.write(f"{x:.6f} {y:.6f} {z:.6f}\n")

        # Generate .mod and move .txt
        mod_file = os.path.join(mod_dir, f"{base}.mod")
        print(f"→ Calling: point2model {txt_file} {mod_file}")
        subprocess.run(['point2model', txt_file, mod_file], check=True)
        os.replace(txt_file, os.path.join(mod_dir, txt_file))

        print(f"{star_file} → {mod_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Relion STAR to .mod models', add_help=True)
    parser.add_argument('--x', type=int, required=True, help='tomogram X size (px)')
    parser.add_argument('--y', type=int, required=True, help='tomogram Y size (px)')
    parser.add_argument('--z', type=int, required=True, help='tomogram Z size (px)')

    # Print help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    process_star_files(args.x, args.y, args.z)

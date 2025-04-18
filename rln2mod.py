import os
import subprocess
import argparse
import starfile
import sys


def process_star_files(x_dim, y_dim, z_dim):
    mod_dir = 'mod'
    os.makedirs(mod_dir, exist_ok=True)

    for star_file in filter(lambda f: f.endswith('_particles.star'), os.listdir('.')):
        # Read STAR data (pick first block if multiple)
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
        with open(txt_file, 'w') as out:
            for x, y, z in zip(xs, ys, zs):
                out.write(f"{x:.6f} {y:.6f} {z:.6f}\n")

        # Generate .mod and move .txt
        mod_file = os.path.join(mod_dir, f"{base}.mod")
        subprocess.run(['point2model', txt_file, mod_file], check=True)
        os.replace(txt_file, os.path.join(mod_dir, txt_file))

        print(f"{star_file} → {mod_file}")


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='Convert Relion STAR to .mod models',
        add_help=True       # this is actually the default
    )
    p.add_argument('--x_dim', type=int, required=True,
                   help='tomogram X size (px)')
    p.add_argument('--y_dim', type=int, required=True,
                   help='tomogram Y size (px)')
    p.add_argument('--z_dim', type=int, required=True,
                   help='tomogram Z size (px)')

    # if you run with no arguments, print the help and exit
    if len(sys.argv) == 1:
        p.print_help(sys.stderr)
        sys.exit(1)

    args = p.parse_args()
    process_star_files(args.x_dim, args.y_dim, args.z_dim)

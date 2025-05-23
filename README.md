# rln2mod.py

A simple script to convert RELION5 `particle.star` coordinates into IMOD `.mod` point models. It will run IMOD's `point2model` on all generated .txt files containing the particle coordinates (top left origin). All `.star` files will be read from the folder from which the script is run.

## Requirements

- [IMOD](https://bio3d.colorado.edu/imod/) must be loaded (e.g., via `module load imod`).
- Python 3 with dependencies:
  ```bash
  pip install starfile
  ```

## Usage

Run the script from the directory containing your `*_particles.star` files:

```bash
module load imod
python rln2mod.py --x_dim <X_SIZE> --y_dim <Y_SIZE> --z_dim <Z_SIZE>
```

- `--x_dim`, `--y_dim`, `--z_dim`: tomogram dimensions in pixels.

All `.mod` models (and intermediate `.txt` files) will be placed in the `mod/` directory.


# rln2mod.py

A simple script to convert Relion STAR particle coordinates into IMOD `.mod` point models.

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
python convert_star.py --x_dim <X_SIZE> --y_dim <Y_SIZE> --z_dim <Z_SIZE>
```

- `--x_dim`, `--y_dim`, `--z_dim`: tomogram dimensions in pixels.

All `.mod` models (and intermediate `.txt` files) will be placed in the `mod/` directory.


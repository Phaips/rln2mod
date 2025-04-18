import os
import subprocess
import shutil
import starfile
 
def parse_star_file(star_file, x_dim, y_dim, z_dim):
    # Load the star file
    data = starfile.read(star_file)
 
    # If data is a dict (multiple data blocks), get the first data block
    if isinstance(data, dict):
        data_block_name = next(iter(data))
        rln = data[data_block_name]
    else:
        rln = data
 
    # Rename the centered coordinates columns for easier access
    rln.rename(columns={
        'rlnCenteredCoordinateXAngst': 'rlnCoordinateX',
        'rlnCenteredCoordinateYAngst': 'rlnCoordinateY',
        'rlnCenteredCoordinateZAngst': 'rlnCoordinateZ'
    }, inplace=True)
 
    # Adjust the coordinates to convert from centered to top-left coordinates
    rln['rlnCoordinateX'] = rln['rlnCoordinateX'] / rln['rlnTomoTiltSeriesPixelSize'] + x_dim / 2
    rln['rlnCoordinateY'] = rln['rlnCoordinateY'] / rln['rlnTomoTiltSeriesPixelSize'] + y_dim / 2
    rln['rlnCoordinateZ'] = rln['rlnCoordinateZ'] / rln['rlnTomoTiltSeriesPixelSize'] + z_dim / 2
 
    # Extract the coordinates as a list of tuples
    coordinates = list(zip(rln['rlnCoordinateX'], rln['rlnCoordinateY'], rln['rlnCoordinateZ']))
    return coordinates
 
def write_txt_file(coordinates, txt_file):
    with open(txt_file, 'w') as f:
        for x, y, z in coordinates:
            f.write(f"{x:.6f} {y:.6f} {z:.6f}\n")
 
def convert_star_to_mod(star_file, txt_file, mod_file, x_dim, y_dim, z_dim):
    coordinates = parse_star_file(star_file, x_dim, y_dim, z_dim)
    write_txt_file(coordinates, txt_file)
     
    # Run the point2model command
    subprocess.run(['point2model', txt_file, mod_file])
 
def move_txt_file(txt_file, mod_dir):
    new_txt_path = os.path.join(mod_dir, os.path.basename(txt_file))
    shutil.move(txt_file, new_txt_path)
 
def process_files(x_dim, y_dim, z_dim):
    star_files = [f for f in os.listdir('.') if f.endswith('_particles.star')]
    mod_dir = 'mod'
     
    if not os.path.exists(mod_dir):
        os.makedirs(mod_dir)
     
    for star_file in star_files:
        base_name = os.path.splitext(star_file)[0]
        txt_file = f"{base_name}.txt"
        mod_file = os.path.join(mod_dir, f"{base_name}.mod")
        convert_star_to_mod(star_file, txt_file, mod_file, x_dim, y_dim, z_dim)
         
        # Move the generated txt file to the mod directory
        move_txt_file(txt_file, mod_dir)
        print(f"Converted {star_file} to {mod_file} and moved {txt_file} to {mod_dir}")
 
if __name__ == "__main__":
    # Replace with the dimensions of the tomogram for visualization
    X_DIM = 1024  # Example X dimension in pixels
    Y_DIM = 1024  # Example Y dimension in pixels
    Z_DIM = 512  # Example Z dimension in pixels
 
    process_files(X_DIM, Y_DIM, Z_DIM)
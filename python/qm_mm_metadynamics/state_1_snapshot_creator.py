import MDAnalysis as mda
import argparse
import os
import glob
import random
import subprocess
import tempfile

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('--state', type=str, help='State to pull from')
parser.add_argument('--ligand', type=str, help='Ligand identifier')

args = parser.parse_args()

# Define directories
curr_directory = os.getcwd()
base_directory = os.path.join(curr_directory.split(args.ligand)[0], args.ligand)
structure_directory = os.path.join(base_directory, 'structure')
meta_state_directory = os.path.join(curr_directory, args.state)

# Locate trajectory and topology files
trajectory = os.path.join(base_directory, f"equil_{args.state}/equil_{args.state}.nc")
prmtop_files = glob.glob(os.path.join(structure_directory, "*.prmtop"))

# Ensure a topology file exists
if not prmtop_files:
    raise FileNotFoundError(f"No .prmtop file found in {structure_directory}")
topology = prmtop_files[0]

# Create the output directory if it doesn't exist
os.makedirs(meta_state_directory, exist_ok=True)

def save_random_rst_frames(topology_file, trajectory_file, meta_state_directory, state, num_frames=25):
    """
    Selects `num_frames` unique random frames from the trajectory and saves them as RST files using cpptraj.

    Parameters:
        topology_file (str): The Amber topology file (.prmtop).
        trajectory_file (str): The trajectory file (.nc, .dcd, etc.).
        meta_state_directory (str): The directory where RST files will be saved.
        state (str): The simulation state used in naming files.
        num_frames (int): Number of unique random frames to extract. Default is 25.
    """
    # Load the trajectory
    u = mda.Universe(topology_file, trajectory_file)
    num_total_frames = len(u.trajectory)

    if num_frames > num_total_frames:
        raise ValueError("Requested more frames than available in the trajectory.")

    random_frames = random.sample(range(num_total_frames), num_frames)  # Select unique random frames
    os.makedirs(meta_state_directory, exist_ok=True)

    for i, frame in enumerate(random_frames, 1):
        rst_filename = f"multiwalk_{state}_{i}.rst"
        rst_location = os.path.join(meta_state_directory, str(i))
        os.makedirs(rst_location, exist_ok=True)
        rst_path = os.path.join(rst_location, rst_filename)

        cpptraj_input=f"""
        parm {topology_file}
        trajin {trajectory_file} {frame} {frame}
        autoimage
        trajout {rst_path} restart
        """

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmpfile:
            tmpfile.write(cpptraj_input)
            tmpfile_path = tmpfile.name

        cpptraj_command = [
            "cpptraj",
            "-i", tmpfile_path,
        ]
        
        try:
            subprocess.run(cpptraj_command, check=True)
            print(f"Successfully extracted frame {frame} to {rst_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error extracting frame {frame}: {e}")
        finally:
            os.remove(tmpfile_path)

    print(f"Saved {num_frames} unique RST snapshots in {meta_state_directory}")

save_random_rst_frames(topology, trajectory, meta_state_directory, args.state)

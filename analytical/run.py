import numpy as np
import os, argparse
from pathlib import Path
import yaml

# Option parser
parser = argparse.ArgumentParser(description="MC/DC verification - analytical")
parser.add_argument("--srun", type=int, default=0)
parser.add_argument("--mpiexec", type=int, default=0)
parser.add_argument("--mpirun", type=int, default=0)
parser.add_argument("--name", type=str, default="ALL")
args, unargs = parser.parse_known_args()

# Get names
name_selected = args.name

# Set MPI command
mpi_command = ""
if args.srun > 0 or args.mpiexec > 0 or args.mpirun > 0:
    if args.srun > 1:
        mpi_command = "srun -n %i" % args.srun
    elif args.mpiexec > 1:
        mpi_command = "mpiexec -n %i" % args.mpiexec
    elif args.mpirun > 1:
        mpi_command = "mpirun -n %i" % args.mpirun

# Create results folder
Path("results").mkdir(parents=True, exist_ok=True)

# Load tasks
with open("task.yaml", "r") as file:
    tasks = yaml.safe_load(file)

# Check if selected name is listed in the task
if name_selected != "ALL" and name_selected not in tasks:
    print(" [ERROR] Selected name '%s' is not in the task list." % name_selected)
    exit()

# Loop over tasks
for name in tasks:
    if name_selected != "ALL" and name != name_selected:
        continue

    # Get into the task folder
    os.chdir(name)

    # Task parameters
    task = tasks[name]
    logN_min = task["logN_min"]
    logN_max = task["logN_max"]
    N_runs = task["N_runs"]

    # Loop over the numbers of particles
    for N_particle in np.logspace(logN_min, logN_max, N_runs, dtype=int):
        # Output name
        output = "output_%i" % (N_particle)

        # Skip if already exist
        if os.path.isfile(output + ".h5"):
            print("Skip (output exists):", name, N_particle)
            continue

        # Command
        command = (
            "%s python input.py --mode=numba --N_particle=%i --output=%s --no-progress_bar --caching"
            % (mpi_command, N_particle, output)
        )
        # Run
        print("Now running:", name, N_particle)
        print("  %s" % command)
        os.system(command)

    # Generate plots
    print("Now generating convergence plots:", name, N_particle)
    os.system("python process.py %i %i %i" % (logN_min, logN_max, N_runs))
    os.system("mv *png ../results")

    # Move back up
    os.chdir(r"..")

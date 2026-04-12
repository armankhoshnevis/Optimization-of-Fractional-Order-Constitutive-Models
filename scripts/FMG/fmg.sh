#!/bin/bash --login

#SBATCH --job-name=FMG_40H1.5G

#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00

# Load necessary modules (Adapt these to your specific cluster environment)
ml purge
ml load Miniforge3
ml load powertools

# Activate the conda environment (Make sure the Conda installation guide is followed)
conda activate Opt_Project

# Print job information
echo "Job started at $(date)"
echo "Running on host $(hostname)"

# Run the Python script
# Note: Ensure you are in the correct directory or provide absolute paths
python fmg_main.py --HS 40 --GnP '1.5GnP'

echo "Job finished at $(date)"
# Optimization of Fractional-Order Constitutive Models

Welcome to the documentation for the `Optimization-of-Fractional-Order-Constitutive-Models` repository.

This package provides a robust, physics-informed data-driven framework to calibrate generalized-order viscoelastic constitutive models to Dynamic Mechanical Analysis (DMA) master curves of polyurea nanocomposites with varied Hard Segment Weight Fractions (HSWF) and exfoliaded Graphene nano-Platelet (xGnP) weight fractions. It leverages Global Particle Swarm Optimization (PSO) to deterministically identify model parameters (characteristic moduli, relaxation times, and fractional exponents) that best describe the time-temperature superposed (TTS) storage and loss moduli of a material over multiple decades of frequency. By utilizing generalized-order models, the highly parsimoneous framework achieves high fidelity with only a handful of physically interpretable parameters.

## Repository Structure
* **`configs/`**: Configuration files for setting up saving file path, experimental data info, parameter ranges, and optimization parameters.
* **`datasets/`**: Synthetic experimental dataset for deterministic calibration.
* **`notebooks/`**: Jupyter notebook equivalents of the python codes for interactive use.
* **`scripts/`**: Main python scripts and utils functions for optimization.
* **`results/`**: Output directories for optimized parameters and visualization.

## Installation
First, clone the repository and navigate into the project directory:
```bash
git clone git@github.com:armankhoshnevis/Optimization-of-Fractional-Order-Constitutive-Models.git
cd Optimization-of-Fractional-Order-Constitutive-Models
```

### Option A: Python venv & pip (Recommended for Running Locally)
If it is preferred to use standard Python virtual environments locally, `pip` alongside the `requirements.txt` file can be used. Then, execute the following commands:
```bash
python -m venv env

# On Windows:
.\env\Scripts\activate

# On macOS/Linux:
source env/bin/activate

pip install -r requirements.txt
```

### Option B: Conda (Recommended for Running on Clusters)
If it is preferred to run the codes on a cluster, `environment.yml` file is used to ensure exact dependency and Python version matching. Then, execute the following commands:
```bash
module load Miniforge3 # Replace with your specific cluster's module if different
conda env create -f environment.yml
conda activate Opt_Project
```

## Quick Run
### Running Locally
Once your environment is activated (via Conda or venv), navigate to the `script` directory and execute the Python files directly from your terminal:
```bash
cd scripts/FMG
python fmg_main.py --HS 20 --GnP '0.0GnP'
```

### Running on a SLURM Cluster
If you are running the inference on a cluster that uses the SLURM workload manager, a sample batch script (`MCMC_FMG.sh` and `MCMC_FMM.sh`) is provided. The script is pre-configured to activate the UQ_Project conda environment.
```bash
cd script/FMG
sbatch fmg.sb
```

**Note:** The script's output and any errors will be automatically logged to standard `.out` and `.err` files in the working directory.

## Documentation
Please refer to this [link](https://armankhoshnevis.github.io/Optimization-of-Fractional-Order-Constitutive-Models/) for more comprehensive documentations.

## Citation Requirements
If you use this software, please cite it and its corresponding paper, as:



- Software citation:
  - APA style: Khoshnevis, A. (2026). Optimization of Fractional-Order Constitutive Models (Version 1.0.0) [Computer software]. https://github.com/armankhoshnevis/Optimization-of-Fractional-Order-Constitutive-Models

  - BibTeX entry:<br>
    @software{Khoshnevis_PSO_Optimization, <br>
    author = {Khoshnevis, Arman},<br>
    license = {Apache-2.0},<br>
    month = mar,<br>
    title = {{Optimization of Fractional-Order Constitutive Models}},<br>
    url = {https://github.com/armankhoshnevis/Optimization-of-Fractional-Order-Constitutive-Models},<br>
    version = {1.0.0},<br>
    year = {2026}<br>
    }

* **Paper citation**:<br>
@article{khoshnevis2025stochastic, <br>
  title={Stochastic Generalized-Order Constitutive Modeling of Viscoelastic Spectra of Polyurea-Graphene Nanocomposites},<br>
  author={Khoshnevis, Arman and Tzelepis, Demetrios A and Ginzburg, Valeriy V and Zayernouri, Mohsen},<br>
  journal={Engineering Reports},<br>
  volume={7},<br>
  number={9},<br>
  pages={e70367},<br>
  year={2025},<br>
  publisher={Wiley Online Library}<br>
}

@article{tzelepis2023polyurea, <br>
  title={Polyurea--graphene nanocomposites—the influence of hard-segment content and nanoparticle loading on mechanical properties}, <br>
  author={Tzelepis, Demetrios A and Khoshnevis, Arman and Zayernouri, Mohsen and Ginzburg, Valeriy V}, <br>
  journal={Polymers}, <br>
  volume={15}, <br>
  number={22}, <br>
  pages={4434}, <br>
  year={2023}, <br>
  publisher={MDPI} <br>
}

## Contributions
This repository is a static archive of the project code. The software is provided "as-is" and is not actively maintained. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more details.
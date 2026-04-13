# Configuration Guide

The optimization pipeline is driven by a YAML configuration file. This file ensures that data extraction from experimental DMA master curves and the subsequent Global PSO calibration are reproducible and easily adjustable.

## Configuration Structure

### Model Selection
* **`model_name`**: Specifies the constitutive law to be used for calibration. Common options include `"FMG_FMG"` for the dual fractional Maxwell gel configuration or `"FMM_FMG"` for the generalized-order model incorporating a second spring-pot exponent ($\beta_1$).

### File Paths
* **`file_path`**: Contains the directory structure for input experimental data and where the optimized results (parameters and error metrics) will be saved.

### Sample and Data Parsing
Each sample entry (e.g., `0.5GnP`) defines how to parse the experimental spreadsheet:

* **`usecols`**: The specific columns in the spreadsheet containing the shifted frequency ($\omega a_T$), storage modulus ($E'$), and loss modulus ($E''$).
* **`skiprows` / `nrows`**: Parameters to isolate the linear viscoelastic region and exclude experimental data points exhibiting high dispersion.
* **`column_names`**: Standardized labels for the data, typically mapped to `["w_freq", "Ep", "Epp"]`.

### Optimization Bounds
* **`bounds`**: Defines the search space for the PSO algorithm.
    * **Lower/Upper**: Arrays specifying the physical limits for model parameters such as characteristic moduli ($E_c$), relaxation times ($\tau_c$), and power-law exponents ($\alpha, \beta$).

### PSO Hyper-parameters
* **`max_it`**: The maximum number of iterations for each optimization run (standard setting is 6,000).
* **`n_pop`**: The swarm population size (standard setting is 200).
* **`n_runs`**: Specifies the number of independent optimization runs to account for the stochastic nature of the PSO. Running multiple iterations (e.g., 50 runs) allows for the calculation of mean values and standard deviations to ensure parameter robustness.
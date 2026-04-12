# Theoretical Background & Methodology

## Fractional Viscoelastic Models
The core of this modeling framework relies on the Fractional Maxwell Model (FMM) and its specialized form, the Fractional Maxwell Gel (FMG). 

* **FMM**: Utilizes two spring-pot elements in series and is characterized by four parameters $(E_c, \tau_c, \alpha, \beta)$.
* **FMG**: Represents a limiting case where the exponent $\beta$ approaches zero, capturing the elastic behavior of materials beyond their gel point.

## Parallel Network Configurations
To accurately model microphase-separated polyurea nanocomposites, the framework configures fractional branches in parallel to represent the filler/soft phase and the percolated hard phase:

1. **FMG-FMG Model**: Uses two parallel FMG branches (totaling 6 parameters).
2. **FMM-FMG Model**: Uses an FMM branch for the soft phase and an FMG branch for the hard phase (totaling 7 parameters).

Given the relatively low meterial presence of graphene nanoplatelet, a separate parallel branch is not considered and included in the model.

![FMM–FMG and FMG–FMG models](images/Models.jpg)

## Morphological Constraint

**Explanation**

Polyurea nanocomposites are characterized by a microphase-separated morphology, with an effective length scale, $L$, representing the average distance between adjacent hard domains. The viscoelastic theory relies on the assumption that the material behaves as a single homogeneous body without internal vibrations. Therefore, the analysis must be restricted to processes occurring on length scales greater than $L$, or frequencies below a "phononic bandgap" threshold, where acoustic waves scatter at the hard-soft interfaces and can be safely neglected. 

**Definition and Formula**

To enforce this physical limitation, the framework introduces a novel dimensionless number, $\mathcal{N}_P$, which acts essentially as the inverse of a Deborah number. It mandates that the material's relaxation time scale $\tau$ must be greater than the time it takes for an acoustic wave to propagate across the domain distance $L/c$:

$$\mathcal{N}_P = \frac{L}{c\tau} = \left[\frac{\rho}{E}\right]^{1/2} \frac{L}{\tau} \le 1$$

where $\rho$ is the material density, $E$ is the Young's modulus, and $c = \sqrt{E/\rho}$ is the speed of sound.

**Ultimate Form Implemented in Optimization**

By hypothesizing that this dimensionless parameter $\mathcal{N}_P$ must be equivalent for both the soft and hard phases to maintain the validity of the Time-Temperature Superposition (TTS), and by neglecting negligible density differences between the two phases, the framework ties the characteristic moduli and relaxation times of both branches together. This yields the final constraint implemented during the PSO calibration:

$$\tau_{c,1} \sqrt{E_{c,1}} \cong \tau_{c,2} \sqrt{E_{c,2}}$$

## Global PSO Calibration

**Algorithm and Objective**

The identification of the fractional model parameters (6 parameters for the FMG-FMG model and 7 for the FMM-FMG model) is performed using a Global Particle Swarm Optimization (PSO) algorithm. The PSO minimizes a scalar multi-objective cost function to concurrently fit the model to both the storage and loss moduli:

$$\min_{q} \left( w_1 g_1(q) + w_2 g_2(q) \right)$$

where $w_1$ and $w_2$ are weights, each set to $1/2$, and $q$ represents the vector of fitting parameters. 

The cost function for each individual modulus ($g_1$ for storage $E'$ and $g_2$ for loss $E''$) is computed as the sum of the squares of the logarithmic difference between experimental data and model predictions across all data points ($N_d$):

$$g_1(q) = \sum_{i=1}^{N_d} \left( \log \frac{E'_{exp,i}}{E'_{model,i}} \right)^2, \quad g_2(q) = \sum_{i=1}^{N_d} \left( \log \frac{E''_{exp,i}}{E''_{model,i}} \right)^2$$

This logarithmic approach is essential for accurately capturing the behavior of materials whose moduli vary by several orders of magnitude across the frequency spectrum.

**Relative Error Assessment**

To evaluate the final fitting quality, a normalized relative error is defined as:

$$\text{Error} = \sqrt{ \frac{w_1 g_1(q) + w_2 g_2(q)}{w_1 \sum_{i=1}^{N_d} (\log E'_{exp,i})^2 + w_2 \sum_{i=1}^{N_d} (\log E''_{exp,i})^2} } \times 100$$

**Settings and Stochasticity**

Each independent optimization run is configured with a swarm population size of 200 and evaluates a total of 6,000 iterations. Because PSO is an inherently stochastic algorithm, the calibration process is independently executed 50 times. The mean values of the optimized parameters across these 50 runs are extracted as the final parameter set, while their standard deviations are calculated to guarantee robustness and ensure the absence of multi-modality in the parameter space.
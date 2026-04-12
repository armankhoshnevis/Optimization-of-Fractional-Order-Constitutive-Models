# Analysis of Optimization Results

After executing the independent PSO runs, a systematic post-processing protocol is applied to filter out sub-optimal solutions and derive statistically robust model parameters.

## Filtering and Refinement
Due to the stochastic nature of the Global Particle Swarm Optimization (PSO), individual runs may occasionally converge to local minima with higher error values. To maintain the highest predictive accuracy, the framework implements a strict selection criterion:

* **Error Thresholding**: Results are retained only if their relative error is within 1% of the minimum error found across all 50 independent runs.
* **Outlier Removal**: Optimized results corresponding to larger Logarithmic Squared Error (LSE) values are discarded to ensure the final statistics are not skewed by sub-optimal convergence.
* **Exponent Ordering**: In some optimization runs, $\alpha_1 > \beta_1$ does not hold and we manually swap the values.

## Statistical Characterization
Once the results are filtered, the framework computes the statistical properties of the identified parameter set:

* **Mean Values**: The mean of each model parameter is calculated from the refined population of successful runs. These mean values represent the "nominal" material properties for the constitutive law.
* **Standard Deviation**: Standard deviations are calculated to assess the reliability of the optimization. Consistently low standard deviations (typically $\mathcal{O}(10^{-4})$ or lower) indicate the absence of multi-modality in the parameter space and confirm that the algorithm has found a stable, absolute minimum.

## Model Visualization
The final verification of the calibration is performed by plotting the model response against the experimental DMA master curves.

* **Mean Parameter Response**: The storage ($E'$) and loss ($E''$) moduli are generated using the calculated mean values of the optimized parameters.
* **Validation**: This visual comparison confirms that the model accurately captures the broad transition regions and power-law behavior of the material over the entire frequency spectrum, typically achieving a relative error of less than 2%.

![Actual experimental data and FMM-FMG model response for (a) 20, (b) 30, and (d) 40 HSWF cases](images/Experimental_Data.png)
import ast
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def constitutive_model(model_params, w_freq):
    """Calculate the storage and loss moduli based on the fractional-order constitutive model.
    Args:
        model_params (array-like): A list of 6 model parameters values [E_c1, tau_c1, alpha_1, beta_1, E_c2, alpha_2].
        w_freq (array-like): An array of angular frequencies at which to evaluate the moduli.
    Returns:
        Ep (numpy array): The storage modulus at each frequency.
        Epp (numpy array): The loss modulus at each frequency.
    """
    # Unpack parameters
    Ec1, tauc1, alpha_1, beta_1 = model_params[0:4]
    Ec2, alpha_2 = model_params[4:6]
    beta2 = 0

    # Enforce the constraint
    tauc2 = tauc1 * np.sqrt(Ec1 / Ec2)    
    
    # Organize for iteration
    Ecs = [Ec1, Ec2]
    taucs = [tauc1, tauc2]
    alphas = [alpha_1, alpha_2]
    betas = [beta_1, beta2]

    # Initialize storage and loss moduli
    Ep = np.zeros_like(w_freq)
    Epp = np.zeros_like(w_freq)

    # Calculate storage and loss moduli
    for i in range(2):
        # Calculate trigonometric terms
        ca = np.cos(0.5 * np.pi * alphas[i])
        cb = np.cos(0.5 * np.pi * betas[i])
        sa = np.sin(0.5 * np.pi * alphas[i])
        sb = np.sin(0.5 * np.pi * betas[i])
        cab = np.cos(0.5 * np.pi * (alphas[i] - betas[i]))

        # Vectorized frequency calculations
        w_tau = w_freq * taucs[i]

        # Caculate the denominator
        denom = 1 + w_tau**(alphas[i] - betas[i]) * cab + w_tau**(2 * (alphas[i] - betas[i]))

        # Calculate the numerators
        num_Ep = Ecs[i] * (w_tau**alphas[i] * ca + w_tau**(2 * alphas[i] - betas[i]) * cb)
        num_Epp = Ecs[i] * (w_tau**alphas[i] * sa + w_tau**(2 * alphas[i] - betas[i]) * sb)

        # Calculate equivalent storage and loss moduli
        Ep += num_Ep / denom
        Epp += num_Epp / denom
    
    return Ep, Epp

def objective_function(model_params, w_freq, Ep_exp, Epp_exp, weights=[0.5, 0.5]):
    """Calculate the objective function value for the given model parameters.
    Args:        
        model_params (array-like): A list of 6 model parameters values [E_c1, tau_c1, alpha_1, beta_1, E_c2, alpha_2].
        w_freq (array-like): An array of angular frequencies at which to evaluate the moduli.
        Ep_exp (array-like): An array of experimental storage modulus values corresponding to w_freq.
        Epp_exp (array-like): An array of experimental loss modulus values corresponding to w_freq.
        weights (list): A list of two weights for the storage and loss modulus terms in the objective function.
    Returns:
        cost_function (float): The calculated objective function value."""
    # Calculate model predictions
    Ep_model, Epp_model = constitutive_model(model_params, w_freq)

    # Calculate the cost function using logarithmic differences
    term1 = np.linalg.norm(np.log(Ep_model) - np.log(Ep_exp))**2
    term2 = np.linalg.norm(np.log(Epp_model) - np.log(Epp_exp))**2

    # Combine the terms with weights
    cost_function = weights[0] * term1 + weights[1] * term2

    return cost_function

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    config['bounds']['lower'] = np.array(config['bounds']['lower'], dtype=float)
    config['bounds']['upper'] = np.array(config['bounds']['upper'], dtype=float)
    
    return config

def run_pso(obj_func, pso_params, data_args):
    """Run Particle Swarm Optimization (PSO) to obtain model parameters.

    Args:
        obj_func (callable): The objective function to minimize, which takes model parameters and additional data arguments as input.
        pso_params (dict): A dictionary containing the PSO parameters (n_pop, max_it, var_min, var_max, n_var, c1, c2, inertia_coeff).
        data_args (tuple): A tuple containing the additional arguments required by the objective function (w_freq, Ep_exp, Epp_exp).

    Returns:
        g_best_pos (array): The best position (optimized model parameters) found by the PSO algorithm.
        g_best_cost (float): The cost associated with the best position.
        best_costs (array): An array containing the best costs for each iteration.
    """
    # Unpack PSO parameters
    n_pop = pso_params['n_pop']
    max_it = pso_params['max_it']
    var_max, var_min = pso_params['var_max'], pso_params['var_min']
    n_var = pso_params['n_var']
    c1, c2 = pso_params['c1'], pso_params['c2']
    inertia_coeff = pso_params['inertia_coeff']

    # Set velocity limits
    max_vel = 0.2 * (var_max - var_min)
    min_vel = -max_vel

    # Initialization
    particle_pos = np.random.uniform(var_min, var_max, (n_pop, n_var))
    particle_vel = np.zeros((n_pop, n_var))
    particle_cost = np.array([obj_func(p, *data_args) for p in particle_pos])

    p_best_pos = particle_pos.copy()
    p_best_cost = particle_cost.copy()

    g_best_idx = np.argmin(p_best_cost)
    g_best_pos = p_best_pos[g_best_idx].copy()
    g_best_cost = p_best_cost[g_best_idx]

    best_costs = np.zeros(max_it)

    # Main Loop
    for it in range(max_it):
        # Update inertia coefficient
        w = inertia_coeff[it]

        # Generate random numbers for velocity update
        r1 = np.random.rand(n_pop, n_var)
        r2 = np.random.rand(n_pop, n_var)
        
        # Update velocity
        particle_vel = (w * particle_vel +
                        c1 * r1 * (p_best_pos - particle_pos) +
                        c2 * r2 * (g_best_pos - particle_pos))
        
        # Apply velocity limits
        particle_vel = np.clip(particle_vel, min_vel, max_vel)

        # Update position
        particle_pos += particle_vel
        
        # Apply position limits
        particle_pos = np.clip(particle_pos, var_min, var_max)

        # Evaluate cost and update personal and global bests
        for i in range(n_pop):
            particle_cost[i] = obj_func(particle_pos[i], *data_args)

            if particle_cost[i] < p_best_cost[i]:
                p_best_pos[i] = particle_pos[i].copy()
                p_best_cost[i] = particle_cost[i]

                if p_best_cost[i] < g_best_cost:
                    g_best_pos = p_best_pos[i].copy()
                    g_best_cost = p_best_cost[i]
        
        # Store best cost for current iteration
        best_costs[it] = g_best_cost

        if (it + 1) % 100 == 0:
            print(f"Iteration {it+1}: Best Cost = {g_best_cost:.4e}")
    
    return g_best_pos, g_best_cost, best_costs

def modify_results(df, sf, file_path, HS, GnP):
    """Filter optimization results with LSE greater than sf * min(LSE)

    Args:
        df (pandas.DataFrame): The DataFrame containing the optimization results.
        sf (float): The scaling factor for the LSE threshold.
        file_path (str): The base file path for saving results.
        HS (int): The HSWF value.
        GnP (str): The GnP value.
    
    Returns:
        modified_df (pandas.DataFrame): The modified DataFrame containing only the mean and std of optimization results within the LSE threshold.
    """
    threshold = sf * df['LSE'].min()
    modified_df = df.loc[df['LSE'] <= threshold].copy()

    swap_mask = modified_df['alpha_1'] < modified_df['beta_1']
    modified_df.loc[swap_mask, ['alpha_1', 'beta_1']] = modified_df.loc[swap_mask, ['beta_1', 'alpha_1']].to_numpy()

    modified_df.describe().loc[['mean', 'std']].to_csv(file_path + f"/{HS}HS_{GnP}_Opt_Params_MeanStd.csv")
    return modified_df

def plot_results(df, modified_df, file_path, HS, GnP):
    """Plot the variation of optimized model parameters over run numbers.

    Args:
        df (pandas.DataFrame): The DataFrame containing the optimization results.
        modified_df (pandas.DataFrame): The modified DataFrame containing only the optimization results within the LSE threshold.
        file_path (str): The base file path for saving results.
        HS (int): The HSWF value.
        GnP (str): The GnP value.
    """
    _, ax = plt.subplots(int(np.ceil(len(modified_df.columns[:-1]) / 2)), 2, figsize=(15, 15))
    ax = ax.flatten()
    for idx, col in enumerate(df.columns[:-1]):
        ax[idx].plot(range(len(df)), df[col], '*-')
        ax[idx].set_xlabel('Run')
        ax[idx].set_ylabel(col)
        ax[idx].set_xticks(range(len(df)))
        ax[idx].set_ylim([df[col].min() * 0.9, df[col].max() * 1.1])
        ax[idx].ticklabel_format(style='plain', axis='y')
    ax[-1].remove()
    plt.tight_layout()
    plt.savefig(file_path + f"/{HS}HS_{GnP}_Opt_Params_Variation.png", dpi=300)
    plt.show()
    plt.close()

    _, ax = plt.subplots(int(np.ceil(len(modified_df.columns[:-1]) / 2)), 2, figsize=(15, 15))
    ax = ax.flatten()
    for idx, col in enumerate(modified_df.columns[:-1]):
        ax[idx].plot(range(len(modified_df)), modified_df[col], '*-')
        ax[idx].set_xlabel('Run')
        ax[idx].set_ylabel(col)
        ax[idx].set_xticks(range(len(modified_df)))
        ax[idx].set_ylim([modified_df[col].min() * 0.9, modified_df[col].max() * 1.1])
        ax[idx].ticklabel_format(style='plain', axis='y')
    ax[-1].remove()
    plt.tight_layout()
    plt.savefig(file_path + f"/{HS}HS_{GnP}_Opt_Params_Variation_Modified.png", dpi=300)
    plt.show()
    plt.close()

def plot_opt_results(file_path, HS, GnP, w_freq_exp, Ep_exp, Epp_exp, run_num):
    """Plot optimized storage and loss moduli against experimental data, and the cost history of optimization runs.

    Args:
        file_path (_type_): _description_
        HS (_type_): _description_
        GnP (_type_): _description_
        w_freq_exp (_type_): _description_
        Ep_exp (_type_): _description_
        Epp_exp (_type_): _description_
        run_num (int): The run number for which to plot the cost history.
    """
    opt_params_mean = pd.read_csv(
        file_path + f"/{HS}HS_{GnP}_Opt_Params_MeanStd.csv",
        index_col=0
        ).drop(columns=['tau_c2']).loc['mean'].values[:-2]

    final_results_df = pd.read_csv(file_path + f"/{HS}HS_{GnP}_Opt_Params_Runs.csv")
    
    Ep_opt, Epp_opt = constitutive_model(opt_params_mean, w_freq_exp)
    plt.loglog(w_freq_exp, Ep_exp, 'o', label='Experimental Storage Modulus')
    plt.loglog(w_freq_exp, Epp_exp, 'o', label='Experimental Loss Modulus')
    plt.loglog(w_freq_exp, Ep_opt, linewidth=4, label='Optimized Storage Modulus')
    plt.loglog(w_freq_exp, Epp_opt, linewidth=4, label='Optimized Loss Modulus')
    plt.xlabel('Shifted Frequency (rad/s)')
    plt.ylabel('Modulus (Pa)')
    plt.legend()
    plt.savefig(file_path + f"/{HS}HS_{GnP}_Opt_Params_Fit.png", dpi=300)
    plt.show()
    plt.close()

    plt.loglog(ast.literal_eval(final_results_df.loc[run_num]['Cost_History']), '*')
    plt.xlabel('Iteration')
    plt.ylabel('Best Cost')
    plt.savefig(file_path + f"/{HS}HS_{GnP}_Opt_Params_CostHistory.png", dpi=300)
    plt.show()
    plt.close()
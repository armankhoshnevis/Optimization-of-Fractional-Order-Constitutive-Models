from fmm_utils import (
    constitutive_model,
    objective_function,
    load_config,
    run_pso,
    modify_results,
    plot_results,
    plot_opt_results
)
import numpy as np
import pandas as pd

import argparse

# Load data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--HS', type=int, default=20, help='HSWF content percentage (e.g., 20 for 20% HSWF)')
    parser.add_argument('--GnP', type=str, default='0.0GnP', help='String identifier for GnP content (e.g., "0.5GnP" for 0.5% GnP)')
    args = parser.parse_args()
    HS = args.HS
    GnP = args.GnP

    config = load_config(f"../../config/FMM/{HS}HSWF_FMM_Config.yaml")

    df_exp = pd.read_excel(
        "../../dataset/Master_Curves_Synthetic.xlsx",
        sheet_name=f"{HS}HS",
        usecols=config["samples"][GnP]["usecols"],
        skiprows=config["samples"][GnP]["skiprows"],
        nrows=config["samples"][GnP]["nrows"],
        names=config["samples"][GnP]["column_names"],
        header=None
    )

    w_freq_exp = df_exp["w_freq"].values
    Ep_exp = df_exp["Ep"].values
    Epp_exp = df_exp["Epp"].values

    # Define optimization hyper-parameters (Clerc & Kennedy)
    var_min = config["bounds"]["lower"]
    var_max = config["bounds"]["upper"]
    n_var = len(var_min)

    inertia_coeff = np.linspace(0.9, 0.4, config['pso']['max_it'])
    kappa, phi1, phi2 = 1, 2.01, 2.01
    phi = phi1 + phi2
    chi = 2 * kappa / abs(2 - phi - np.sqrt(phi**2 - 4 * phi))

    pso_params = {
        'n_pop': config['pso']['n_pop'],
        'max_it': config['pso']['max_it'],
        'n_runs': config['pso']['n_runs'],
        'var_min': var_min,
        'var_max': var_max,
        'n_var': n_var,
        'inertia_coeff': inertia_coeff,
        'c1': chi * phi1,
        'c2': chi * phi2,
    }

    # Define the objective function coefficients and the remaining data arguments for optimization
    obj_func_coeff = [0.5, 0.5]
    data_args = (w_freq_exp, Ep_exp, Epp_exp, obj_func_coeff)

    n_run = config['pso']['n_runs']
    results = []

    for run in range(n_run):
        print(f"\n###### Starting Run {run+1}/{n_run} ######")
        opt_params, best_cost, cost_history = run_pso(objective_function, pso_params, data_args)
        
        # Add the constrained parameter (tau_c2) to the optimized parameters for saving only
        full_opt_params = np.insert(opt_params, 5, opt_params[1] * np.sqrt(opt_params[0] / opt_params[4]))
        
        # Calculate Error (LSE)
        datanorm = obj_func_coeff[0] * np.linalg.norm(np.log(Ep_exp))**2 + obj_func_coeff[1] * np.linalg.norm(np.log(Epp_exp))**2
        lse = np.sqrt(best_cost / datanorm) * 100
        
        results.append(list(full_opt_params) + [best_cost, lse, cost_history.tolist()])

    # Save Results
    final_results_df = pd.DataFrame(
        results,
        columns=['E_c1', 'tau_c1', 'alpha_1', 'beta_1', 'E_c2', 'tau_c2', 'alpha_2', 'Best_Cost', 'LSE', 'Cost_History'],
    )
    final_results_df.to_csv(f"{config['file_path']['results']}/{HS}HS_{GnP}_Opt_Params_Runs.csv", index=False)

    print("\nOptimization Complete.")

    final_results_modified_df = modify_results(final_results_df.copy(), 1.01, config['file_path']['results'], HS, GnP)
    plot_results(final_results_df, final_results_modified_df, config['file_path']['results'], HS, GnP)
    plot_opt_results(config['file_path']['results'], HS, GnP, w_freq_exp, Ep_exp, Epp_exp, 0)

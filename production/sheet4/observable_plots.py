from tools import *
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 10})


chains_metro = list()
betas_metro = list()
filenames_metro = [f"chains/metro_{T}" for T in range(100, 201, 10)]
filenames_metro += [f"chains/metro_{T}" for T in range(210, 241, 2)]
filenames_metro += [f"chains/metro_{T}" for T in range(250, 401, 10)]
for filename in filenames_metro:
    print(f"loading {filename}")
    chain = ChainAnalyzer(filename)
    chain.calc_measurements()
    chain.calc_autocorrelation_function()
    chain.calc_autocorrelation_time()
    chain.calc_corrected_error()
    _, _, t_int_c, t_int_chi = chain.calc_error_c_and_chi_propagation()
    chain.calc_error_c_and_chi_corrected_bootstrap(num_samples = 1000, autocorr_time_e = t_int_c, autocorr_time_m = t_int_chi)
    betas_metro.append(chain.beta)
    chains_metro.append(chain)


chains_wolff = list()
betas_wolff = list()
filenames_wolff = [f"chains/wolff_{T}" for T in range(210, 241, 2)]
for filename in filenames_wolff:
    print(f"loading {filename}")
    chain = ChainAnalyzer(filename)
    chain.calc_measurements()
    chain.calc_autocorrelation_function()
    chain.calc_autocorrelation_time()
    chain.calc_corrected_error()
    _, _, t_int_c, t_int_chi = chain.calc_error_c_and_chi_propagation()
    chain.calc_error_c_and_chi_corrected_bootstrap(num_samples = 1000, autocorr_time_e = t_int_c, autocorr_time_m = t_int_chi)
    betas_wolff.append(chain.beta)
    chains_wolff.append(chain)


def create_plot(betas, chains, temp_limits = None):
    #prepare the data
    temps = np.array([1/beta for beta in betas])
    Es = np.array([chain.E_mean for chain in chains])
    Ms = np.array([chain.M_mean for chain in chains])
    Cs = np.array([chain.heat_capacity_density for chain in chains])
    Chis = np.array([chain.magnetic_susceptibility_density for chain in chains])
    E_errs = np.array([chain.E_corrected_error for chain in chains])
    M_errs = np.array([chain.M_corrected_error for chain in chains])
    C_errs = np.array([chain.heat_capa_corrected_bootstrap_err for chain in chains])
    Chi_errs = np.array([chain.magn_susc_corrected_bootstrap_err for chain in chains])

    #set up the fgure
    fig, [[ax_E, ax_M], [ax_C, ax_Chi]] = plt.subplots(figsize = (5.9, 4), nrows = 2, ncols = 2, sharex = True)

    # prepare x axes
    ax_C.set_xlabel("Temp T")
    ax_Chi.set_xlabel("Temp T")
    if temp_limits:
        ax_C.set_xlim(temp_limits[0], temp_limits[1])
        ax_Chi.set_xlim(temp_limits[0], temp_limits[1])
    else:
        ax_C.set_xlim(min(temps), max(temps))
        ax_Chi.set_xlim(min(temps), max(temps))

    #prepare y axes
    ax_E.set_ylabel(r"Energy, $e$")
    ax_M.set_ylabel(r"Magnetisation., $m$")
    ax_C.set_ylabel(r"Heat capa., $c$")
    ax_Chi.set_ylabel(r"Mag. suscep., $\chi$")
    DE = max(Es) - min(Es)
    ax_E.set_ylim(min(Es) - 0.05*DE, max(Es) + 0.05*DE)
    ax_M.set_ylim(0, 1.1*max(Ms))
    ax_C.set_ylim(0, 1.1*max(Cs))
    ax_Chi.set_ylim(0, 1.1*max(Chis))

    #plot :)
    ax_E.plot(temps, Es, color = "red")
    ax_E.fill_between(temps, Es - E_errs, Es + E_errs, color = "red", alpha = 0.4)

    ax_M.plot(temps, Ms, color = "blue")
    ax_M.fill_between(temps, Ms - M_errs, Ms + M_errs, color = "blue", alpha = 0.3)

    ax_C.plot(temps, Cs, color = "coral")
    ax_C.fill_between(temps, Cs - C_errs, Cs + C_errs, color = "coral", alpha = 0.4)

    ax_Chi.plot(temps, Chis, color = "royalblue")
    ax_Chi.fill_between(temps, Chis - Chi_errs, Chis + Chi_errs, color = "royalblue", alpha = 0.3)

    fig.tight_layout()
    plt.show()

create_plot(betas_metro, chains_metro)
create_plot(betas_metro, chains_metro, temp_limits = (2.1, 2.4))
create_plot(betas_wolff, chains_wolff)

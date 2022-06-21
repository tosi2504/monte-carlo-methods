import tools
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
plt.rcParams.update({'font.size': 10})

chains = dict()
chains_list = list()
betas = list()
for ID in ["3846", "4347", "5000"]:
    chains[ID] = tools.ChainAnalyzer(filename = "chains/" + ID + ".ising")
    chains[ID].calc_measurements()
    chains[ID].calc_autocorrelation_function()
    chains[ID].calc_autocorrelation_time()
    chains[ID].calc_corrected_error()
    chains_list.append(chains[ID])
    betas.append(int(ID)/10000)

# autocorrelation plot
fig, axEs = plt.subplots(figsize = (5.9, 5.9), nrows = 3, ncols = 1, sharex = False)
axMs = []
for axE in axEs:
    axMs.append(axE.twinx())
for axE, axM, chain, beta in zip(axEs, axMs, chains_list, betas):
    X_E = np.arange(len(chain.E_autocorrelation))
    X_M = np.arange(len(chain.M_autocorrelation))
    axE.scatter(X_E, chain.E_autocorrelation, color = "black", marker = "x", s = 10)
    axM.scatter(X_M, chain.M_autocorrelation, color = "blue", marker = "x", s = 10)
    axM.spines["right"].set_color("blue")
    axM.yaxis.label.set_color("blue")
    axM.tick_params(axis='y', colors='blue')
    my_text = axM.text(0.985, 0.94, f'beta = {beta:0.3f}',
        verticalalignment='top', horizontalalignment='right',
        transform=axM.transAxes,
        color='black', fontsize=10)
    my_text.set_bbox(dict(boxstyle='round', facecolor='white', edgecolor="black", alpha = 0.7))
    axE.grid()
    axE.set_ylim(0, 1.09)
    axM.set_ylim(0, 1.09)
    #fitting now
    fit_func = lambda x, tau: np.exp(-x/tau)
    [tau_E], _ = curve_fit(fit_func, X_E, chain.E_autocorrelation)
    [tau_M], _ = curve_fit(fit_func, X_M, chain.M_autocorrelation)
    axM.plot(X_E, fit_func(X_E, tau_E), color="grey", label = r"fit: $\tau =$" + f"{tau_E:0.3f}")
    axM.plot(X_M, fit_func(X_M, tau_M), color="royalblue", label = r"fit: $\tau =$" + f"{tau_M:0.3f}")
    axM.legend(loc="right")
    print(f"BETA {beta} | TEMP {1/beta:0.1f}")
    print("    ENERGY-DATA")
    print(f"        t_int = {chain.E_autocorr_time:0.4f} and t_fit = {tau_E:0.4f}")
    print(f"        <e> = {chain.E_mean:0.7f}, std-error = {chain.E_corrected_error:0.7f}")
    print("    MAGNETISATION-DATA")
    print(f"        t_int = {chain.M_autocorr_time:0.4f} and t_fit = {tau_M:0.4f}")
    print(f"        <m> = {chain.M_mean:0.7f}, std-error = {chain.M_corrected_error:0.7f}")
    print(" ")

axEs[-1].set_xlabel(r"Time difference, $t$")
# axEs[-1].set_xlim(0,100)
axEs[1].set_ylabel(r"Autocorr. $\rho_E(t)$ on $E$")
axMs[1].set_ylabel(r"Autocorr. $\rho_M(t)$ on $M$")
axEs[0].set_xlim(0, 30)
axEs[1].set_xlim(0, 400)
axEs[2].set_xlim(0, 30)
fig.tight_layout()
plt.show()

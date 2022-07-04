from tools import *
import numpy as np
import matplotlib.pyplot as plt
import math
plt.rcParams.update({'font.size': 10})


chains_metro = list()
betas_metro = list()
e_taus_metro = list()
m_taus_metro = list()
filenames_metro = [f"chains/metro_{T}" for T in range(210, 241, 2)]
for filename in filenames_metro:
    print(f"loading {filename}")
    chain = ChainAnalyzer(filename)
    chain.calc_measurements()
    chain.calc_autocorrelation_function()
    chain.calc_autocorrelation_time()
    e_taus_metro.append(chain.E_autocorr_time)
    m_taus_metro.append(chain.M_autocorr_time)
    betas_metro.append(chain.beta)
    chains_metro.append(chain)


chains_wolff = list()
betas_wolff = list()
e_taus_wolff = list()
m_taus_wolff = list()
filenames_wolff = [f"chains/wolff_{T}" for T in range(210, 241, 2)]
for filename in filenames_wolff:
    print(f"loading {filename}")
    chain = ChainAnalyzer(filename)
    chain.calc_measurements()
    chain.calc_autocorrelation_function()
    chain.calc_autocorrelation_time()
    e_taus_wolff.append(chain.E_autocorr_time*chain.acc_therm.mean()/chain.grid_size/chain.grid_size)
    m_taus_wolff.append(chain.M_autocorr_time*chain.acc_therm.mean()/chain.grid_size/chain.grid_size)
    betas_wolff.append(chain.beta)
    chains_wolff.append(chain)




fig, [ax_E, ax_M] = plt.subplots(figsize = (5.9, 3), ncols = 2, nrows = 1)

# prepare the data
temps = np.array([1/beta for beta in betas_metro])

# prepare x axes
ax_E.set_xlabel("Temperature, $T$")
ax_M.set_xlabel("Temperature, $T$")
ax_E.set_ylabel(r"Energy autocorr.-time $\tau_{\mathrm{int, E}}$")
ax_M.set_ylabel(r"Mag. autocorr.-time $\tau_{\mathrm{int, M}}$")
ax_E.set_xlim(min(temps), max(temps))
ax_M.set_xlim(min(temps), max(temps))
ax_E.set_ylim(0, max(e_taus_wolff + e_taus_metro)*1.05)
ax_M.set_ylim(0, max(m_taus_wolff + m_taus_metro)*1.05)

# plot now
ax_E.plot(temps, e_taus_metro, color = "red", label ="Metro")
ax_E.plot(temps, e_taus_wolff, color = "blue", label ="Wolff")
ax_E.legend(loc = "upper left")
ax_E.grid()

ax_M.plot(temps, m_taus_metro, color = "red", label ="Metro")
ax_M.plot(temps, m_taus_wolff, color = "blue", label ="Wolff")
ax_M.legend(loc = "upper left")
ax_M.grid()


fig.tight_layout()
plt.show()

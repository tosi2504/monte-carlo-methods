from tools import *
import numpy as np
import matplotlib.pyplot as plt
import math
plt.rcParams.update({'font.size': 10})



chains_wolff = list()
betas_wolff = list()
clusters = list()
cluster_errs = list()
filenames_wolff = [f"chains/wolff_{T}" for T in range(210, 241, 2)]
for filename in filenames_wolff:
    print(f"loading {filename}")
    chain = ChainAnalyzer(filename)
    cluster_data = chain.acc_therm/chain.grid_size/chain.grid_size
    clusters.append(cluster_data.mean())
    rho_positive = ChainAnalyzer.calc_positive_autocorrelation(cluster_data)
    t_int = ChainAnalyzer.integrated_autocorrelation_time(rho_positive)
    print(t_int)
    cluster_errs.append(cluster_data.std() * math.sqrt(2*t_int / len(cluster_data)))
    betas_wolff.append(chain.beta)
    chains_wolff.append(chain)

clusters = np.array(clusters)
cluster_errs = np.array(cluster_errs)

fig, ax = plt.subplots(figsize = (5.9, 3))
ax.set_xlabel(r"Temperature, $T$")
ax.set_ylabel(r"Cluster size, $\frac{\langle n \rangle}{V}$")
ax.set_xlim(2.1, 2.4)
ax.set_ylim(0, max(clusters)*1.05)
temps = [1/beta for beta in betas_wolff]
ax.plot(temps, clusters, color = "black")
ax.fill_between(temps, clusters - cluster_errs, clusters + cluster_errs, color = "black", alpha = 0.3)
fig.tight_layout()
plt.show()

import tools
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
plt.rcParams.update({'font.size': 10})
chains = dict()
chains_list = list()
betas = list()


print(" ")
for ID in ["3846", "4347", "5000"]:
    chains[ID] = tools.ChainAnalyzer(filename = "chains/" + ID + ".ising")
    chains[ID].calc_measurements()
    chains[ID].calc_autocorrelation_function()
    chains[ID].calc_autocorrelation_time()
    chains[ID].calc_corrected_error()
    chains[ID].calc_error_c_and_chi_propagation()
    chains[ID].calc_error_c_and_chi_blocking(num_blocks = 20)
    chains[ID].calc_error_c_and_chi_bootstrap(num_samples = 1000)
    print(f"BETA {chains[ID].beta} | TEMP {1/chains[ID].beta:0.1f}")
    print(f"    PROPAGATION:   err_c = {chains[ID].heat_capa_propagation_err:0.6f}     err_chi = {chains[ID].magn_susc_propagation_err:0.6f}")
    print(f"    BLOCKING:      err_c = {chains[ID].heat_capa_blocking_err:0.6f}     err_chi = {chains[ID].magn_susc_blocking_err:0.6f}")
    print(f"    BOOTSTRAP:     err_c = {chains[ID].heat_capa_bootstrap_err:0.6f}     err_chi = {chains[ID].magn_susc_bootstrap_err:0.6f}")
    print(" ")
    chains_list.append(chains[ID])
    betas.append(int(ID)/10000)



# heat_capas = list()
# magn_suscs = list()
# for i in range(100):
#     chain = tools.ChainAnalyzer(filename = f"chains/critical{i}.ising")
#     chain.calc_measurements()
#     heat_capas.append(chain.heat_capacity_density)
#     magn_suscs.append(chain.magnetic_susceptibility_density)
# heat_capas = np.array(heat_capas)
# magn_suscs = np.array(magn_suscs)
# print(f"BETA {1/2.3} | TEMP {2.3}")
# print(f"    MULTIPLE_CHAINS:   err_c = {heat_capas.std():0.6f}     err_chi = {magn_suscs.std():0.6f}")

# the above commented code will lead to this output
print("""BETA 0.4347826086956522 | TEMP 2.3
    MULTIPLE_CHAINS:   err_c = 0.029870     err_chi = 2.912681""")

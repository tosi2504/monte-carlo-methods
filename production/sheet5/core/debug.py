from pyIsing import IsingModel as IM
import numpy as np
import matplotlib.pyplot as plt
import time
import math

N = 16
eps = 0.01
numLeaps = 20
T = 2
beta = 1/T
print(beta)
ising = IM(N, 100)
number_of_sweeps = 100000


energies = list()
mags = list()
accepted = 0
for i in range(number_of_sweeps):
    print(i)
    if ising.hmc_one_step(beta, numLeaps, eps): # seems to work yay! actually does.
        accepted += 1
    energies.append(ising.E/N/N)
    mags.append(math.sqrt(ising.M_vec_x**2 + ising.M_vec_y**2)/N/N)

print(accepted/number_of_sweeps)

fig , [axE, axM] = plt.subplots(nrows = 2, ncols = 1, sharex = True)
axE.plot(energies)
axM.plot(mags)
plt.show()

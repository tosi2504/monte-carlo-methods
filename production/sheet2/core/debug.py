from pyIsing import IsingModel as IM
import numpy as np
import matplotlib.pyplot as plt
import time

N = 64
ising = IM(N, 2)


energies = list()
mags = list()
accepted = 0
for i in range(10000):
    print(ising.wolff(1/2.3), i)
    energies.append(ising.E /64/64)
    mags.append(abs(ising.M)/64/64)


plt.plot(energies)
plt.plot(mags)
plt.show()

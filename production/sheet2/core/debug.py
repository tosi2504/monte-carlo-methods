from pyIsing import IsingModel as IM
import numpy as np
import matplotlib.pyplot as plt

N = 32
ising = IM(N, 2)


E = list()
M = list()
for i in range(10000):
    print(i, "acceptance", ising.metropolis_sweep(0.4)/N**2)
    E.append(ising.E)
    M.append(ising.M)


plt.plot(E)
plt.plot(M)
plt.show()

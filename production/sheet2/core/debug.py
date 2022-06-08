from pyIsing import IsingModel as IM
import numpy as np
import matplotlib.pyplot as plt
import time

N = 64
ising = IM(N, 2)


start = time.perf_counter()
accepted = 0
for i in range(10000):
    accepted += ising.metropolis_sweep(0.5)
print(time.perf_counter() - start)
print("Acceptance:", accepted/10000/64/64)

from tools import *
import numpy as np

for T in range(100, 401, 10):
    print("Temperatur", T/100)
    chain = ChainGenerator(grid_size = 64, beta = 1/T*100, seed =  int(T))
    chain.run_metropolis(15000)
    chain.thermalize(5000)
    chain.export(f"chains/metro_{T}")

for T in range(210, 241, 2):
    print("Temperatur", T/100)
    chain = ChainGenerator(grid_size = 64, beta = 1/T*100, seed = int(T*100))
    chain.run_metropolis(15000)
    chain.thermalize(5000)
    chain.export(f"chains/metro_{T}")

for T in range(210, 241, 2):
    print("Temperatur", T/100)
    chain = ChainGenerator(grid_size = 64, beta = 1/T*100, seed = int(T*10000))
    chain.run_wolff(15000)
    chain.thermalize(5000)
    chain.export(f"chains/wolff_{T}")

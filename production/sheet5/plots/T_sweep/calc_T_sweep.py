import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from tools import ChainAnalyzer
from os import listdir
import matplotlib.pyplot as plt


temps = list()
mags = list()
errs = list()

for filename in listdir("chains_T_sweep"):
    chain = ChainAnalyzer("chains_T_sweep/" + filename)
    chain.calc_measurements()
    chain.calc_autocorrelation_function()
    chain.calc_autocorrelation_time()
    chain.calc_corrected_error()
    temps.append(round(1/chain.beta, 1))
    mags.append(chain.M_mean)
    errs.append(chain.M_corrected_error)
    print(filename, "done")

with open("T_sweep_data.txt", "w") as file:
    for temp, mag, err in zip(temps, mags, errs):
        file.write(f"{temp} {mag} {err}\n")

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from os import listdir
from tools import ChainAnalyzer
import matplotlib.pyplot as plt


directory = "chains_beta0_3"
filenames = listdir(directory)

numLeapss = list()
leapsizes = list()
E_autocorr_times = list()
for filename in filenames:
    chain = ChainAnalyzer(directory+"/"+filename)
    chain.calc_autocorrelation_function()
    chain.calc_autocorrelation_time()
    numLeapss.append(chain.numLeaps)
    leapsizes.append(chain.leapsize)
    E_autocorr_times.append(chain.E_autocorr_time)
    print("sheesh")
# save the data
with open("computer_time_high_T_data.txt", "w") as file:
    for numLeaps, leapsize, t_int in zip(numLeapss, leapsizes, E_autocorr_times):
        file.write(f"{numLeaps} {leapsize} {2*t_int*numLeaps}"+'\n')

from os import listdir
from tools import ChainAnalyzer
import matplotlib.pyplot as plt


directory = "chains_beta1_5"
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
    print("ssheesh")

fig = plt.figure()
ax = fig.add_subplot(projection = "3d")
ax.scatter(numLeapss, leapsizes, E_autocorr_times)
ax.set_yscale("log")
plt.show()

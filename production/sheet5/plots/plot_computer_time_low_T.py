import matplotlib.pyplot as plt
import numpy as np
import math


with open("computer_time_low_T_data.txt", "r") as file:
    lines = [line.strip().split(" ") for line in file.readlines()]

numLeapss = list()
leapsizes = list()
c_times = list()
for numLeaps, leapsize, c_time in lines:
    numLeapss.append(int(numLeaps))
    leapsizes.append(float(leapsize))
    if math.log10(float(c_time)) < 6:
        c_times.append(float(c_time))
    else:
        c_times.append(1e6)
numLeapss = np.array(numLeapss)
leapsizes = np.array(leapsizes)
c_times = np.array(c_times)


fig = plt.figure()
ax = fig.add_subplot(projection = "3d")
ax.plot_trisurf(numLeapss, np.log10(leapsizes), np.log10(c_times), cmap = plt.cm.viridis)
ax.set_zlim(2, 6)
plt.show()

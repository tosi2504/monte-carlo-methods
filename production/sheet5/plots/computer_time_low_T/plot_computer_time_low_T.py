import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import griddata


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


def interpolate(x, y, z, method = "linear", fx = 10, fy = 10):
    len_x = len(set(x))
    len_y = len(set(y))
    points = np.array([x,y]).T
    grid_X, grid_Y = np.meshgrid(np.linspace(min(x), max(x), fx*len_x,), np.linspace(min(y), max(y), fy*len_y))
    grid_Z = griddata(points, z, (grid_X, grid_Y), method = method)
    return grid_X, grid_Y, grid_Z


fig = plt.figure(figsize = (5, 3))
ax = fig.add_subplot(111)
CS = ax.contourf(*interpolate(numLeapss, np.log10(leapsizes), np.log10(c_times)), cmap= plt.cm.viridis)
ax.scatter(numLeapss, np.log10(leapsizes), color = "black", marker = "o", s = 0.5)
ax.set_xlabel(r"leaps, $n_\tau$")
ax.set_ylabel(r"Stepsize $\log_{10}\,dt$")
cbar = fig.colorbar(CS)
cbar.ax.set_ylabel(r"comp. time, $\log_{10} t_C$")
fig.tight_layout()
plt.show()

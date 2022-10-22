import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata


filenames = ["data.txt", "data2.txt"]
lines = list()
for filename in filenames:
    with open(filename, "r") as file:
        lines += [line.strip().split(" ") for line in file.readlines()]

temps = list()
stepsizes = list()
e_times = list()
for line in lines:
    temps.append(float(line[0]))
    stepsizes.append(float(line[1]))
    if float(line[2]) > 10000 or line[2] == "nan":
        e_times.append(10000)
    else:
        e_times.append(float(line[2]))
temps = np.array(temps)
stepsizes = np.array(stepsizes)
e_times = np.array(e_times)

def interpolate(x, y, z, method = "linear", fx = 10, fy = 10):
    len_x = len(set(x))
    len_y = len(set(y))
    points = np.array([x,y]).T
    grid_X, grid_Y = np.meshgrid(np.linspace(min(x), max(x), fx*len_x,), np.linspace(min(y), max(y), fy*len_y))
    grid_Z = griddata(points, z, (grid_X, grid_Y), method = method)
    return grid_X, grid_Y, grid_Z


fig = plt.figure(figsize = (5, 3))
ax = fig.add_subplot(111)
CS = ax.contourf(*interpolate(temps, np.log10(stepsizes), np.log10(e_times)), cmap= plt.cm.viridis)
ax.scatter(temps, np.log10(stepsizes), color = "black", marker = "o", s = 0.5)
ax.set_xlabel("Temp. $T$")
ax.set_ylabel(r"Stepsize $\log_{10}\,dt$")
ax.axvline(1.1, color = "blue", linewidth = 2)
cbar = fig.colorbar(CS)
cbar.ax.set_ylabel(r"Autocorr. time, $\log_{10}\,\tau_{int, E}$")
fig.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams.update({'font.size': 11})
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

#load data
Ns = np.array(10**np.linspace(1,6,101), dtype = int)
data = np.genfromtxt("data.txt", dtype = float, delimiter = ",")
# data is NxM array i.e. data[n,m]

# plot for exercise 1
fig = plt.figure(figsize = (5.9, 3))
ax, axHisto = fig.subplots(nrows = 1, ncols = 2)

ax.set_xscale("log")
ax.set_xlabel("Sample size, N")
ax.set_ylabel(r"Sample average $\overline{\cos}$")
for data_set in data.T:
    ax.scatter(Ns, data_set, color="black", s = 2)
ax.axvline(Ns[20], color="red")
ax.axvline(Ns[50], color="blue")
ax.set_xlim(10, 1000000)
ax.axhline(0.606, color = "green")
ax.set_axisbelow(True)
ax.grid()

axHisto.hist(data[20], color = "red")
axHisto.hist(data[50], color = "blue")
axHisto.set_xlabel(r"Sample average $ \overline{\cos} $")
axHisto.set_ylabel(r"Distribution, $\rho(\overline{\cos})$")
axHisto.axvline(0.606, color = "green")
axHisto.grid()

fig.tight_layout()
fig.savefig("fig1.pdf")


# plot for exercise 2
stdev = np.std(data, axis=1)
fig = plt.figure(figsize = (5.9, 3))
ax = fig.subplots(nrows = 1, ncols = 1)

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Sample size, N")
ax.set_ylabel(r"Sample std. dev., $s_{\bar{f}}$")
ax.set_xlim(10, 1000000)
ax.grid()
ax.scatter(Ns, stdev, color = "black", s = 4)
fitfunc = lambda N,a,b: a*N**b
popt, _ = curve_fit(fitfunc, Ns, stdev, sigma = stdev)
print("Optimized params: ", *popt)
ax.plot(Ns, fitfunc(Ns, *popt), color = "blue", label = r"Fit $a N ^ b$ " + f": a = {popt[0]:1.2f}, b = {popt[1]:1.2f}")
ax.legend()

fig.tight_layout()
fig.savefig("fig2.pdf")
plt.show()

print("red line:", Ns[20])
print("blue line:", Ns[50])

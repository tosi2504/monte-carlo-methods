import matplotlib.pyplot as plt


with open("T_sweep_data.txt", "r") as file:
    lines = [line.strip().split(" ") for line in file.readlines()]

temps, mags, errs = list(), list(), list()
for line in lines:
    temps.append(float(line[0]))
    mags.append(float(line[1]))
    errs.append(float(line[2]))


fig = plt.figure(figsize = (5.9, 4))
ax = fig.add_subplot(111)
ax.errorbar(x = temps, y = mags, yerr = errs, capsize = 5, fmt = "x")
ax.set_xlabel("temperature, $T$")
ax.set_ylabel("magnetisation, $M$")
ax.set_xlim(0, 3)
ax.set_ylim(0, 1)
ax.grid()
fig.tight_layout()
plt.show()

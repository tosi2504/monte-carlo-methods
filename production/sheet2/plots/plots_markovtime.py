import tools
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 10})
import numpy as np

# load data
chains = dict()
chains_list = list()
betas = list()
for ID in ["3846", "4347", "5000"]:
    chains[ID] = tools.ChainAnalyzer(filename = "chains/" + ID + ".ising")
    chains_list.append(chains[ID])
    betas.append(int(ID)/1000)


# thermalisation plot
fig, axEs = plt.subplots(figsize = (5.9, 4), nrows = 3, ncols = 1, sharex = True)
axMs = []
for axE in axEs:
    axMs.append(axE.twinx())
for axE, axM, chain, beta in zip(axEs, axMs, chains_list, betas):
    axE.plot(chain.E, color = "black", linewidth = 1.2)
    axM.plot(chain.M, color = "blue", linewidth = 1.2)
    axM.spines["right"].set_color("blue")
    axM.yaxis.label.set_color("blue")
    axM.tick_params(axis='y', colors='blue')
    my_text = axM.text(0.985, 0.92, f'beta = {beta:0.3f}',
        verticalalignment='top', horizontalalignment='right',
        transform=axM.transAxes,
        color='black', fontsize=10)
    my_text.set_bbox(dict(boxstyle='round', facecolor='white', edgecolor="black", alpha = 0.7))

axEs[-1].set_xlabel(r"Markov time, $t_M$")
axEs[-1].set_xlim(0,100)
axEs[1].set_ylabel(r"Energy per site, $e = E/V$")
axMs[1].set_ylabel(r"Magnetisation per site, $m = M/V$")
fig.tight_layout()
plt.show()


# general plot
fig, axEs = plt.subplots(figsize = (5.9, 4), nrows = 3, ncols = 1, sharex = True)
axMs = []
for axE in axEs:
    axMs.append(axE.twinx())
for axE, axM, chain, beta in zip(axEs, axMs, chains_list, betas):
    axE.plot(chain.E, color = "black", linewidth = 0.6)

    axM.plot(chain.M, color = "blue", linewidth = 0.6)
    axM.spines["right"].set_color("blue")
    axM.yaxis.label.set_color("blue")
    axM.tick_params(axis='y', colors='blue')
    my_text = axM.text(0.985, 0.92, f'beta = {beta:0.3f}',
        verticalalignment='top', horizontalalignment='right',
        transform=axM.transAxes,
        color='black', fontsize=10)
    my_text.set_bbox(dict(boxstyle='round', facecolor='white', edgecolor="black", alpha = 0.7))


axEs[-1].set_xlabel(r"Markov time, $t_M$")
axEs[-1].set_xlim(0,10000)
axEs[1].set_ylabel(r"Energy per site, $e = E/V$")
axMs[1].set_ylabel(r"Magnetisation per site, $m = M/V$")
fig.tight_layout()
plt.show()

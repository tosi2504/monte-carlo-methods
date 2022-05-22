import tools


chains = dict()
for ID in ["3846", "4347", "5000"]:
    chains[ID] = tools.ChainAnalyzer(filename = "chains/" + ID + ".ising")

for ID, chain in chains.items():
    chain.plot_energy_and_mag()

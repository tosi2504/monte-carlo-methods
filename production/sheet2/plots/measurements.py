import tools
chains = dict()
chains_list = list()
betas = list()
for ID in ["3846", "4347", "5000"]:
    chains[ID] = tools.ChainAnalyzer(filename = "chains/" + ID + ".ising")
    chains_list.append(chains[ID])
    betas.append(int(ID)/10000)

for beta, chain in zip(betas, chains_list):
    chain.calc_measurements();
    print(beta, chain.E_mean, chain.M_mean, chain.heat_capacity_density, chain.magnetic_susceptibility_density)

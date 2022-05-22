import tools

# lets generate the chains
for beta in [1/T for T in [2.0, 2.3, 2.6]]:
    chain = tools.ChainGenerator(beta = beta, grid_size = 64, seed = int(beta*100))
    chain.run(100000)
    chain.plot()
    chain.thermalize_live()
    chain.export(f"./chains/{int(beta*10000)}.ising")

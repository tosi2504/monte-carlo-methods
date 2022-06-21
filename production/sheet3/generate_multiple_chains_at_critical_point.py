import tools

for i in range(50, 100, 1):
    chain = tools.ChainGenerator(grid_size = 64, beta = 1/2.3, seed = i * 3)
    chain.run(N_steps = 109000)
    chain.thermalize(N_therm = 10000)
    chain.export(f"chains/critical{i}.ising")
    print(i)

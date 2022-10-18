from tools import ChainGenerator
import numpy as np
import random
random.seed(0)

generator = ChainGenerator(grid_size = 16
                        , beta = 1.5
                        , seed = random.randint(0, 1000000))
generator.run_hmc(100000, 3, 0.01)
generator.plot()
generator.clear_buffer()

for numLeaps in range(1,7):
    for leapsize in 10**np.linspace(-2.25, -0.25, 7, dtype=np.double):
        generator.run_hmc(200000, numLeaps, leapsize)
        print(numLeaps, leapsize)
        generator.thermalize(0)
        generator.export(f"chains_beta1_5/{numLeaps}_{leapsize}")
        generator.clear_buffer()



import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from tools import ChainGenerator
import numpy as np
import random
random.seed(0)

generator = ChainGenerator(grid_size = 16
                        , beta = 0.3
                        , seed = random.randint(0, 1000000))
generator.run_hmc(100000, 3, 0.01)
generator.plot()
generator.clear_buffer()

for numLeaps in range(1,7):
    for leapsize in 10**np.linspace(0.05, 0.65, 3, dtype=np.double):
        generator.run_hmc(200000, numLeaps, leapsize)
        print(numLeaps, leapsize)
        generator.thermalize(0)
        generator.export(f"chains_beta0_3/{numLeaps}_{leapsize}")
        generator.clear_buffer()



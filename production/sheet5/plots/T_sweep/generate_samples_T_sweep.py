import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from tools import ChainGenerator
import numpy as np


generator = ChainGenerator(grid_size = 16
                            , beta = 1 / 0.1
                            , seed = 1337)

generator.run_hmc(100000, 1, 0.1)
generator.plot()
generator.clear_buffer()

for T in np.linspace(0.1, 3.0, 30):
    generator.beta = 1/T
    generator.run_hmc(200000, 1, 0.1)
    generator.thermalize(10000)
    generator.export(f"chains_T_sweep/{round(T*10)}.txt")
    generator.clear_buffer()
    print("sheeesh")

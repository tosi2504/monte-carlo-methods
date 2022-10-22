import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from tools import ChainGenerator, ChainAnalyzer
import numpy as np

generator = ChainGenerator(grid_size = 16, beta = 1 / 0.1, seed = 0)


with open("data2.txt", "w") as file:
    for T in np.linspace(0.1, 3.0, 30):
        generator.beta = 1 / T;
        generator.run_hmc(N_steps = 100000, numLeaps = 1, leapsize = 0.1)
        generator.clear_buffer();

        for dt in 10**np.linspace(-0.25+2/11, -0.25+2/11*6, 6):
            print(f"Now working on T: {T}, dt: {dt}")
            generator.run_hmc(N_steps = 100000, numLeaps = 1, leapsize = dt, count = False)
            generator.thermalize(0)
            generator.export("temp_chain.txt")
            generator.clear_buffer()
            analyzer = ChainAnalyzer("temp_chain.txt")
            analyzer.calc_measurements()
            analyzer.calc_autocorrelation_function()
            analyzer.calc_autocorrelation_time()
            file.write(f"{T} {dt} {analyzer.E_autocorr_time} {analyzer.M_autocorr_time}\n")



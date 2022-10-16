from pyIsing import IsingModel
import numpy as np
import matplotlib.pyplot as plt
import math


class ChainGenerator:
    def __init__(self, grid_size, beta, seed):
        self.grid_size = grid_size
        self.beta = beta
        self.IsingModel = IsingModel(grid_size, seed)
        self.E = list()
        self.M = list()
        self.numLeaps = -1
        self.leapsize = -1

    def run_metropolis(self, N_steps):
        for i in range(N_steps):
            self.IsingModel.metropolis_sweep(self.beta)
            self.E.append(self.IsingModel.E/(self.grid_size**2))
            self.M.append(self.IsingModel.M/(self.grid_size**2))
            print(i)

    def run_hmc(self, N_steps, numLeaps, leapsize):
        for i in range(N_steps):
            self.IsingModel.hmc_one_step(self.beta, numLeaps, leapsize)
            self.E.append(self.IsingModel.E/(self.grid_size**2))
            self.M.append(self.IsingModel.M/(self.grid_size**2))
            print(i)
        self.numLeaps = numLeaps
        self.leapsize = leapsize

    def plot(self):
        fig = plt.figure()
        axE = fig.add_subplot()
        axM = axE.twinx()
        axE.plot(self.E, color = "red")
        axM.plot(self.M, color = "blue")
        plt.show()

    def thermalize(self, N_therm):
        self.N_therm = N_therm

    def thermalize_live(self):
        N_therm = int(input("How many sweeps do you want to discard: "))
        self.thermalize(N_therm)

    def export(self, filename):
        with open(filename, "w") as file:
            file.write(f"# {self.beta} {self.grid_size} {self.N_therm} {self.numLeaps} {self.leapsize} in format beta grid_size N_therm numLeaps leapsize\n")
            for e, m in zip(self.E, self.M):
                file.write(f"{e} {m}\n")


class ChainAnalyzer:
    def __init__(self, filename):
        with open(filename, "r") as file:
            lines = [line.strip().split(" ") for line in file.readlines()]
        self.beta = float(lines[0][1])
        self.grid_size = int(lines[0][2])
        self.N_therm = int(lines[0][3])
        self.numLeaps = int(lines[0][4])
        self.leapsize = float(lines[0][5])
        self.E, self.M = np.zeros(len(lines)-2), np.zeros(len(lines)-2)
        for i, line in enumerate(lines[1:-1]):
            self.E[i], self.M[i] = float(line[0]), float(line[1])
        self.N_sweeps = len(lines) - 2
        self.E = np.array(self.E)
        self.M = np.array(self.M)
        self.M_abs = np.abs(self.M)
        self.E_therm = self.E[self.N_therm:]
        self.M_therm = self.M_abs[self.N_therm:]

    def calc_measurements(self):
        self.E_mean = self.E_therm.mean()
        self.M_mean = self.M_therm.mean()
        self.E_var = self.E_therm.var()
        self.M_var = self.M_therm.var()
        self.heat_capacity_density = self.beta**2 * self.grid_size**2 * self.E_var
        self.magnetic_susceptibility_density = self.beta * self.grid_size**2 * self.M_var

    def plot_energy_and_mag(self):
        fig = plt.figure(figsize = (5.9, 2))
        axE = fig.add_subplot()
        axM = axE.twinx()
        axE.set_xlabel(r"Markov time, $N_t$")
        axE.set_ylabel(r"Energy per site, $E$")
        axM.set_ylabel(r"Mag. per site, $|M|$")
        axE.axvline(self.N_therm, color = "black")
        axE.plot(self.E, color="red", label = "E")
        axM.plot(self.M, color="blue", label = "|M|")
        axE.set_xlim(0, self.N_sweeps-1)
        axE.legend()
        fig.tight_layout()
        plt.show()

    @staticmethod
    def calc_positive_autocovariance(chain):
        autocovariance = [np.var(chain)]
        y_plus = chain.mean()
        y_minus = chain.mean()
        stop = False
        N = len(chain)
        for t in range(1, N):
            y_plus = (y_plus * (N - t + 1) - chain[N-t])/(N-t)
            y_minus = (y_minus * (N - t + 1) - chain[t])/(N-t)
            new_autocovariance_val = ((chain[:-t] - y_minus)*(chain[t:] - y_plus)).mean()
            if new_autocovariance_val >= 0:
                autocovariance.append(new_autocovariance_val)
            else:
                break
        return np.array(autocovariance)

    @staticmethod
    def calc_positive_autocorrelation(chain):
        autocorrelation = ChainAnalyzer.calc_positive_autocovariance(chain)
        autocorrelation /= autocorrelation[0]
        return autocorrelation

    @staticmethod
    def integrated_autocorrelation_time(positive_autocorrelation):
        return 0.5 + np.sum(positive_autocorrelation)

    def calc_autocorrelation_function(self):
        self.E_autocorrelation = ChainAnalyzer.calc_positive_autocorrelation(self.E_therm)
        self.M_autocorrelation = ChainAnalyzer.calc_positive_autocorrelation(self.M_therm)

    def calc_autocorrelation_time(self):
        self.E_autocorr_time = ChainAnalyzer.integrated_autocorrelation_time(self.E_autocorrelation)
        self.M_autocorr_time = ChainAnalyzer.integrated_autocorrelation_time(self.M_autocorrelation)

    def calc_corrected_error(self):
        self.E_corrected_error = self.E_therm.std() * math.sqrt(2*self.E_autocorr_time / len(self.E_therm))
        self.M_corrected_error = self.M_therm.std() * math.sqrt(2*self.M_autocorr_time / len(self.M_therm))

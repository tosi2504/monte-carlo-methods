from pyIsing import IsingModel
import numpy as np
import matplotlib.pyplot as plt


class ChainGenerator:
    def __init__(self, grid_size, beta, seed):
        self.grid_size = grid_size
        self.beta = beta
        self.IsingModel = IsingModel(grid_size, seed)
        self.E = list()
        self.M = list()

    def run(self, N_steps):
        for i in range(N_steps):
            self.IsingModel.metropolis_sweep(self.beta)
            self.E.append(self.IsingModel.E/(self.grid_size**2))
            self.M.append(self.IsingModel.M/(self.grid_size**2))
            print(i)

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
            file.write(f"# {self.beta} {self.grid_size} {self.N_therm} in format beta grid_size N_therm\n")
            for e, m in zip(self.E, self.M):
                file.write(f"{e} {m}\n")


class ChainAnalyzer:
    def __init__(self, filename):
        with open(filename, "r") as file:
            lines = [line.strip().split(" ") for line in file.readlines()]
        self.beta = float(lines[0][1])
        self.grid_size = int(lines[0][2])
        self.N_therm = int(lines[0][3])
        self.E, self.M = np.zeros(len(lines)-2), np.zeros(len(lines)-2)
        for i, line in enumerate(lines[1:-1]):
            self.E[i], self.M[i] = float(line[0]), float(line[1])
        self.N_sweeps = len(lines) - 2
        self.E = np.array(self.E)
        self.M = np.array(self.M)
        self.M_abs = np.abs(self.M)
        self.E_therm = self.E[self.N_therm:]
        self.M_therm = self.M[self.N_therm:]
        self.M_therm = self.M_abs[self.N_therm:]

    def calc_statistics(self):
        self.E_mean = self.E_therm.mean()
        self.M_mean = self.M_therm.mean()
        self.E_std = self.E_therm.std()
        self.M_std = self.M_therm.std()

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

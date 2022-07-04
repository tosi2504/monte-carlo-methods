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
        self.acc = list()

    def run_metropolis(self, N_steps):
        for i in range(N_steps):
            self.acc.append(self.IsingModel.metropolis_sweep(self.beta))
            self.E.append(self.IsingModel.E/(self.grid_size**2))
            self.M.append(self.IsingModel.M/(self.grid_size**2))
            print(i)

    def run_wolff(self, N_steps):
        for i in range(N_steps):
            self.acc.append(self.IsingModel.wolff(self.beta))
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
            for e, m, acc in zip(self.E, self.M, self.acc):
                file.write(f"{e} {m} {acc}\n")


class ChainAnalyzer:
    def __init__(self, filename):
        with open(filename, "r") as file:
            lines = [line.strip().split(" ") for line in file.readlines()]
        self.beta = float(lines[0][1])
        self.grid_size = int(lines[0][2])
        self.N_therm = int(lines[0][3])
        self.E, self.M, self.acc = np.zeros(len(lines)-2), np.zeros(len(lines)-2), np.zeros(len(lines)-2)
        for i, line in enumerate(lines[1:-1]):
            self.E[i], self.M[i], self.acc[i] = float(line[0]), float(line[1]), float(line[2])
        self.N_sweeps = len(lines) - 2
        self.E = np.array(self.E)
        self.M = np.array(self.M)
        self.M_abs = np.abs(self.M)
        self.E_therm = self.E[self.N_therm:]
        self.M_therm = self.M_abs[self.N_therm:]
        self.acc_therm = self.acc[self.N_therm:]

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
        return 0.5 + np.sum(positive_autocorrelation[1:])

    def calc_autocorrelation_function(self):
        self.E_autocorrelation = ChainAnalyzer.calc_positive_autocorrelation(self.E_therm)
        self.M_autocorrelation = ChainAnalyzer.calc_positive_autocorrelation(self.M_therm)

    def calc_autocorrelation_time(self):
        self.E_autocorr_time = ChainAnalyzer.integrated_autocorrelation_time(self.E_autocorrelation)
        self.M_autocorr_time = ChainAnalyzer.integrated_autocorrelation_time(self.M_autocorrelation)

    def calc_corrected_error(self):
        self.E_corrected_error = self.E_therm.std() * math.sqrt(2*self.E_autocorr_time / len(self.E_therm))
        self.M_corrected_error = self.M_therm.std() * math.sqrt(2*self.M_autocorr_time / len(self.M_therm))

    def calc_error_c_and_chi_propagation(self):
        dc_dx = self.beta ** 2 * self.grid_size ** 2
        dc_dy = -self.beta ** 2 * self.grid_size ** 2 * 2 * self.E_therm.mean()
        dchi_dx = self.beta * self.grid_size ** 2
        dchi_dy = -self.beta * self.grid_size ** 2 * 2 * self.M_therm.mean()
        eff_obs_c = lambda e: dc_dx*e**2 + dc_dy * e
        eff_obs_chi = lambda m: dchi_dx*m**2 + dchi_dy * m
        err_c, t_int_c = error_propagation(self.E_therm, eff_obs_c)
        err_chi, t_int_chi = error_propagation(self.M_therm, eff_obs_chi)
        self.heat_capa_propagation_err = err_c
        self.magn_susc_propagation_err = err_chi
        return self.heat_capa_propagation_err, self.magn_susc_propagation_err, t_int_c, t_int_chi

    def calc_error_c_and_chi_blocking(self, num_blocks):
        blocks_c = list()
        blocks_chi = list()
        len_block = len(self.E_therm)//num_blocks
        for i in range(num_blocks-1):
            blocks_c.append(self.beta**2 * self.grid_size**2 * self.E_therm[i*len_block:(i+1)*len_block].var())
            blocks_chi.append(self.beta * self.grid_size**2 * self.M_therm[i*len_block:(i+1)*len_block].var())
        blocks_c.append(self.beta**2 * self.grid_size**2 * self.E_therm[(num_blocks-1)*len_block:].var())
        blocks_chi.append(self.beta * self.grid_size**2 * self.M_therm[(num_blocks-1)*len_block:].var())
        blocks_c = np.array(blocks_c)
        blocks_chi = np.array(blocks_chi)
        self.heat_capa_blocking_err = blocks_c.std()/math.sqrt(num_blocks)
        self.magn_susc_blocking_err = blocks_chi.std()/math.sqrt(num_blocks)
        return self.heat_capa_blocking_err, self.magn_susc_blocking_err

    def calc_error_c_and_chi_bootstrap(self, num_samples):
        samples_c = list()
        samples_chi = list()
        for i in range(num_samples):
            sample_E = np.random.choice(a = self.E_therm[::math.ceil(2*self.E_autocorr_time)], size = len(self.E_therm)//math.ceil(2*self.E_autocorr_time))
            sample_M = np.random.choice(a = self.M_therm[::math.ceil(2*self.M_autocorr_time)], size = len(self.M_therm)//math.ceil(2*self.M_autocorr_time))
            samples_c.append(self.beta**2 * self.grid_size**2 * sample_E.var())
            samples_chi.append(self.beta * self.grid_size**2 * sample_M.var())
        samples_c = np.array(samples_c)
        samples_chi = np.array(samples_chi)
        self.heat_capa_bootstrap_err = samples_c.std()
        self.magn_susc_bootstrap_err = samples_chi.std()
        return self.heat_capa_bootstrap_err, self.magn_susc_bootstrap_err

    def calc_error_c_and_chi_corrected_bootstrap(self, num_samples, autocorr_time_e, autocorr_time_m):
        samples_c = list()
        samples_chi = list()
        for i in range(num_samples):
            sample_E = np.random.choice(a = self.E_therm[::math.ceil(2*autocorr_time_e)], size = len(self.E_therm)//math.ceil(2*autocorr_time_e))
            sample_M = np.random.choice(a = self.M_therm[::math.ceil(2*autocorr_time_m)], size = len(self.M_therm)//math.ceil(2*autocorr_time_m))
            samples_c.append(self.beta**2 * self.grid_size**2 * sample_E.var())
            samples_chi.append(self.beta * self.grid_size**2 * sample_M.var())
        samples_c = np.array(samples_c)
        samples_chi = np.array(samples_chi)
        self.heat_capa_corrected_bootstrap_err = samples_c.std()
        self.magn_susc_corrected_bootstrap_err = samples_chi.std()
        return samples_c.std(), samples_chi.std()

def error_propagation(chain, effective_observable):
    obs_chain = effective_observable(chain)
    err_uncorrected = obs_chain.std()/math.sqrt(len(chain))
    t_int = ChainAnalyzer.integrated_autocorrelation_time(ChainAnalyzer.calc_positive_autocorrelation(obs_chain))
    return err_uncorrected * math.sqrt(2 * t_int), t_int

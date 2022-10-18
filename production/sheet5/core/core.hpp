#pragma once

#include <vector>
#include <queue>
#include <deque>
#include <map>
#include <array>
#include <random>
#include <cmath>


using coord_flat = unsigned int;
struct coord_xy {
    unsigned int x, y;
    coord_xy(): x(0), y(0) {}
    coord_xy(unsigned int x, unsigned int y):x(x), y(y) {}
    bool operator<(const coord_xy & other) const {
        if (y < other.y) return true;
        else if (y == other.y) return x < other.x;
        else return false;
    }
};

struct IsingModel {
    // grid properties
    const unsigned int N;
    std::vector<std::array<coord_flat, 4>> nn_lookup;
    std::map<coord_xy, coord_flat> xy_to_flat;
    std::map<coord_flat, coord_xy> flat_to_xy;

    // dynamic variables
    std::vector<double> config;
	std::vector<double> mom;
	std::vector<double> pos;
    double E;
    double M_vec_x;
    double M_vec_y;

    // rng stuff
    std::mt19937 rng;
    std::uniform_real_distribution<> uni_dist;
    std::uniform_int_distribution<> random_site_dist;
	std::normal_distribution<> normal_dist;

    // setup
    IsingModel() = delete;
    IsingModel(unsigned int N, unsigned int seed);
    void init_grid_cold();
    void fill_maps();
    void fill_nn_lookup();

	// observables
	void update_mag();
	void update_energy();
	double calc_energy(const std::vector<double> & config);

    // state update algorithms
    int metropolis_one_step(double beta, coord_flat site, double delta);
    int metropolis_sweep(double beta, double delta);

	double leapfrog(std::vector<double> & pos, std::vector<double> & mom, int numLeaps, double eps, double beta);
	bool hmc_one_step(double beta, int numLeaps, double eps);
};

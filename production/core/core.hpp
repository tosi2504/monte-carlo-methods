#pramga once

#include <vector>
#include <map>
#include <array>
#include <random>
#include <cmath>

using coord_flat = unsigned int;
struct coord_xy { unsigned int x, y; };

struct IsingModel {
    // grid properties
    const unsigned int N;
    std::vector<std::array<coord_flat, 4>> nn_lookup;
    std::map<coord_xy, coord_flat> xy_to_flat;
    std::map<coord_xy, coord_flat> flat_to_xy;

    // dynamic variables
    std::vector<short int> config;
    int E;
    int M;

    // rng stuff
    std::mt19937 rng;
    std::uniform_real_distribution<> uni_dist;

    // setup
    IsingModel() = delete;
    IsingModel(unsigned int N, unsigned int seed);
    void init_grid(double ratio);
    void fill_maps();
    void fill_nn_lookup();

    // state update algorithms
    int metropolis_one_step(double beta);
    int metropolis_sweep(double beta);
};

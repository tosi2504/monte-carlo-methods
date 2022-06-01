#pragma once

#include <vector>
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
    int metropolis_one_step(double beta, coord_flat site);
    int metropolis_sweep(double beta);
    static std::array<double,5> create_lookup(double beta);
    int metropolis_one_step(const std::array<double,5> & lookup, coord_flat site);

    // access
    bool at(unsigned int x, unsigned int y);
    void set(unsigned int x, unsigned int y, bool val);
    int calc_energy();

};

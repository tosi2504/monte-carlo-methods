#include "core.hpp"

// row major matrix convetion applied to lattice
// origin is top left

#include <iostream>


IsingModel::IsingModel(unsigned int N, unsigned int seed): N(N) {
    rng = std::mt19937(seed);
    uni_dist = std::uniform_real_distribution<>(0.0, 1.0);
    random_site_dist = std::uniform_int_distribution<>(0, N*N - 1);
    fill_maps();
    fill_nn_lookup();
    init_grid(0.5);
}

void IsingModel::init_grid(double ratio) {
    config.resize(N*N);
    for (short int & site: config) {
        if (uni_dist(rng) < ratio) {
            site = 1;
        } else {
            site = -1;
        }
    }
    //calc E and M of config
    E = 0;
    M = 0;
    for (coord_flat site = 0; site < N*N; site++) {
        const auto & nn = nn_lookup[site];
        E += - config[site]*config[nn[1]]; // right
        E += - config[site]*config[nn[2]]; // bottom
        M += config[site];
    }
}

void IsingModel::fill_maps() {
    coord_xy xy(0,0);
    for (unsigned int x = 0; x < N; x++) {
        for (unsigned int y = 0; y < N; y++) {
            xy.x = x;
            xy.y = y;
            coord_flat flat = y*N + x;
            xy_to_flat[xy] = flat;
            flat_to_xy[flat] = xy;
        }
    }
}

void IsingModel::fill_nn_lookup() {
    nn_lookup.resize(N*N);
    for (const auto & [xy, flat]: xy_to_flat) {
        coord_xy top = coord_xy(xy.x, (xy.y + N - 1) % N);
        coord_xy bottom = coord_xy(xy.x, (xy.y + 1) % N);
        coord_xy left = coord_xy((xy.x + N - 1) % N, xy.y);
        coord_xy right = coord_xy((xy.x + 1) % N, xy.y);
        nn_lookup[flat] = {xy_to_flat[top], xy_to_flat[right], xy_to_flat[bottom], xy_to_flat[left]};
    }
}

int IsingModel::metropolis_one_step(double beta, coord_flat site) {
    int delta_energy = 0;
    for (coord_flat nn: nn_lookup[site]) {
        delta_energy += config[site]*config[nn];
    }
    delta_energy = 2 * delta_energy;


    if (uni_dist(rng) < std::exp(-delta_energy*beta)) {
        config[site] = config[site]*(-1); // accepted
        E += delta_energy;
        M += 2 * config[site];
        return 1;
    }
    return 0;
}

int IsingModel::metropolis_sweep(double beta) {
    int accepted = 0;
    for (coord_flat site = 0; site < N*N; site++) {
        accepted += metropolis_one_step(beta, site);
    }
    return accepted;
}

std::array<double,5> IsingModel::create_lookup(double beta) {
    std::array<double,5> result;
    for (int i = 0; i < 5; i++) {
        int delta_energy = 4*(i-2);
        result[i] = std::exp(-delta_energy*beta);
    }
    return result;
}

int IsingModel::metropolis_one_step_lookup(const std::array<double,5> & lookup, coord_flat site) {
    int delta_energy = 0;
    for (coord_flat nn: nn_lookup[site]) {
        delta_energy += config[site]*config[nn];
    }


    if (uni_dist(rng) < lookup[delta_energy/2 + 2]) {
        config[site] = config[site]*(-1); // accepted
        E += 2*delta_energy;
        M += 2 * config[site];
        return 1;
    }
    return 0;
}

int IsingModel::wolff(double beta) {
    // init the queue
    std::queue<coord_flat, std::deque<coord_flat>> cluster;

    // choose random site
    coord_flat initial_site = random_site_dist(rng);
    short int initial_spin = config[initial_site];

    // push in the first site
    cluster.push(initial_site);
    flip(initial_site);
    int cluster_size = 1;

    // start the while loop
    while (!cluster.empty()) {
        for (coord_flat nn: nn_lookup[cluster.front()]) {
            if (config[nn] == initial_spin) {
                if (uni_dist(rng) < (1 - std::exp(-2*beta))) {
                    flip(nn);
                    cluster.push(nn);
                    cluster_size += 1;
                }
            }
        }
        cluster.pop();
    }
    return cluster_size;
}


bool IsingModel::at(unsigned int x, unsigned int y) {
    return 1 == config[y*N + x];
}

void IsingModel::set(unsigned int x, unsigned int y, bool val) {
    config[y*N + x] = (val) ? 1 : -1;
    E = calc_energy();
}

void IsingModel::flip(coord_flat site) {
    int delta_energy = 0;
    for (coord_flat nn: nn_lookup[site]) {
        delta_energy += config[site]*config[nn];
    }
    config[site] *= -1;
    E += 2*delta_energy;
    M += 2 * config[site];
}

int IsingModel::calc_energy() {
    int energy = 0;
    for (coord_flat site = 0; site < N*N; site++) {
        energy += -config[site]*config[nn_lookup[site][1]];
        energy += -config[site]*config[nn_lookup[site][2]];
    }
    return energy;
}

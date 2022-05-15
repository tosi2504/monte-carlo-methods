#include "core.hpp"

// row major matrix convetion applied to lattice
// origin is top left


IsingModel::IsingModel(unsigned int N, unsigned int seed): N(N) {
    rng = std::mt19937(seed);
    uni_dist = std::uniform_real_distribution<>(0.0, 1.0);
    fill_maps();
    fill_nn_lookup();
    init_grid(0.5);
}

void IsingModel::init_grid(double ratio) {
    config.resize(N*N);
    for (short int & site: config) {
        if (uni_dist(rng) < ratio) {
            site = -1;
        } else {
            site = 1;
        }
    }
    //calc E and M of config
    E = 0
    M = 0
    for (const auto & [site, nn]: nn_lookup) {
        E += - config[site]*config[nn[1]]; // right
        E += - config[site]*config[nn[2]]; // bottom
        M += config[site];
    }
}

void IsingModel::fill_maps() {
    coord_xy xy;
    for (unsigned int x; x < N; x++) {
        for (unsigned int y; y < N; y++) {
            xy.x = x;
            xy.y = y;
            coord_flat flat = y*N + x;
            xy_to_flat.insert(xy, flat);
            flat_to_xy.insert(flat, xy);
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

    if (uni_dist(rng) < std::exp(-delta_energy)) {
        config[site] *= -1; // accepted
        E += delta_energy;
        M += 2 * config[site];
        return 1;
    }
    return 0;
}

int IsingModel::metropolis_sweep(double beta) {
    accepted = 0;
    for (coord_flat site = 0; site < N*N; site++) {
        accepted += metropolis_one_step(beta, site);
    }
    return accepted
}

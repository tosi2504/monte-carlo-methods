#include "core.hpp"

// row major matrix convetion applied to lattice
// origin is top left

#include <iostream>

IsingModel::IsingModel(unsigned int N, unsigned int seed): N(N) {
    rng = std::mt19937(seed);
    uni_dist = std::uniform_real_distribution<>(0.0, 1.0);
    random_site_dist = std::uniform_int_distribution<>(0, N*N - 1);
	normal_dist = std::normal_distribution<>(0.0, 1.0);
    fill_maps();
    fill_nn_lookup();
    init_grid_cold();
	mom.resize(N*N);
	pos.resize(N*N);
}

void IsingModel::init_grid_cold() {
    config.resize(N*N);
    for (double & site: config) {
        site = 0.0;
    }
    E = (double)-2*N*N;
    M_vec_x = N*N;
    M_vec_y = 0;
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

void IsingModel::update_mag() {
	M_vec_x = 0;
	M_vec_y = 0;
	for (coord_flat site = 0; site < N*N; site++) {
		M_vec_x += std::cos(config[site]);
		M_vec_y += std::sin(config[site]);
	}
}

void IsingModel::update_energy() {
	E = 0;
	for (coord_flat site = 0; site < N*N; site++) {
		for (int i = 0; i < 2; i++) {
			E -= std::cos(config[site] - config[nn_lookup[site][i]]);
		}
	}
}

double IsingModel::calc_energy(const std::vector<double> & some_config) {
	double result = 0;
	for (coord_flat site = 0; site < N*N; site++) {
		for (int i = 0; i < 2; i++) {
			result -= std::cos(some_config[site] - some_config[nn_lookup[site][i]]);
		}
	}
	return result;
}

int IsingModel::metropolis_one_step(double beta, coord_flat site, double delta) {
    double new_spin = config[site] + (2*uni_dist(rng) - 1)*delta;
    double delta_energy = 0;
    for (coord_flat nn: nn_lookup[site]) {
        // de is new - old
        delta_energy += -std::cos(new_spin - config[nn]) + std::cos(config[site] - config[nn]);
    }

    if (uni_dist(rng) < std::exp(-delta_energy*beta)) {
        E += delta_energy;
        M_vec_x += -std::cos(config[site]) + std::cos(new_spin);
        M_vec_y += -std::sin(config[site]) + std::sin(new_spin);
        config[site] = new_spin; // accepted
        return 1;
    }
    return 0;
}

int IsingModel::metropolis_sweep(double beta, double delta) {
    int accepted = 0;
    for (coord_flat site = 0; site < N*N; site++) {
        accepted += metropolis_one_step(beta, site, delta);
    }
    return accepted;
}

double IsingModel::leapfrog(std::vector<double> & pos, std::vector<double> & mom, int numLeaps, double eps, double beta) {
	// inital half step
	for (coord_flat site = 0; site < N*N; site++) {
		double dV_dq = 0;
		for (coord_flat nn: nn_lookup[site]) {
			dV_dq += beta*std::sin(pos[site] - pos[nn]);
		}
		mom[site] -= dV_dq * eps / 2;
	}

	// full steps
	for (int t = 1; t < numLeaps; t++) {
		for (coord_flat site = 0; site < N*N; site++){
			pos[site] += mom[site] * eps;
		}
		for (coord_flat site = 0; site < N*N; site++){
			double dV_dq = 0;
			for (coord_flat nn: nn_lookup[site]) {
				dV_dq += beta*std::sin(pos[site] - pos[nn]);
			}
			mom[site] -= dV_dq * eps;
		}
	}

	// final half step
	for (coord_flat site = 0; site < N*N; site++){
		pos[site] += mom[site] * eps;
	}
	double final_kinetic = 0;
	for (coord_flat site = 0; site < N*N; site++){
		double dV_dq = 0;
		for (coord_flat nn: nn_lookup[site]) {
			dV_dq += beta*std::sin(pos[site] - pos[nn]);
		}
		mom[site] -= dV_dq * eps / 2;
		final_kinetic += mom[site]*mom[site];
	}
	return final_kinetic/2;
}

bool IsingModel::hmc_one_step(double beta, int numLeaps, double eps) {
	// initialize random momenta and copy spins
	double init_kinetic = 0;
	for (coord_flat site = 0; site < N*N; site++) {
		// momenta
		mom[site] = normal_dist(rng);
		init_kinetic += mom[site]*mom[site];
		//positions
		pos[site] = config[site];
	}
	init_kinetic = init_kinetic/2;

	// leapfrog
	double final_kinetic = leapfrog(pos, mom, numLeaps, eps, beta);

	// accept-reject
	double final_E = calc_energy(pos);
	double dH = final_kinetic - init_kinetic + beta * (final_E - E);
	if (uni_dist(rng) < std::exp(-dH)) {
		config = pos;
		update_mag();
		E = final_E;
		return true;
	} else {
		return false;
	}
}

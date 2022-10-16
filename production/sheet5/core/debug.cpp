#include "core.hpp"
#include <iostream>
#include <vector>
#include <cmath>

int main () {
    unsigned int N = 64;
    IsingModel im(N,0);
    double T = 2.0;
    double delta = 0.1;

    std::vector<double> energy(100000);
    std::vector<double> mag(100000);
    for (int i = 0; i < 100000; i++) {
        im.metropolis_sweep(T, delta);
        energy[i] = im.E;
        mag[i] = std::sqrt(im.M_vec_x*im.M_vec_x + im.M_vec_y*im.M_vec_y);
    }
    

}

#include "core.hpp"
#include <iostream>
#include <time.h>


int main () {
    unsigned int N = 64;
    IsingModel im(N,0);
    auto lookup = IsingModel::create_lookup(0.4);
    time_t start = time(NULL);
    for (int i = 0; i < 100000; i++) {
        for (coord_flat site = 0; site < N*N; site++) {
            im.metropolis_one_step(lookup, site);
        }
    }
    time_t end = time(NULL);
    std::cout << (double)(end - start) << std::endl;
}

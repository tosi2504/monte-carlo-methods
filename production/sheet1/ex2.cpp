#include <vector>
#include <random>
#include <cmath>
#include <array>
#include <iostream>
#include <fstream>

# define SEED 1


template <typename config_t, typename measure_t>
measure_t measurement_average(measure_t (*measurement)(config_t config), const std::vector<config_t> & sample) {
    measure_t result = measure_t(0);
    for (auto & config: sample) {
        result += measurement(config);
    }
    return result/sample.size();
}


void fill_vector_with_normal(std::vector<double> & sample, double mean, double sigma, std::mt19937 & rng) {
	std::normal_distribution<> norm_dist{mean, sigma};
    for (double & val: sample) {
		val = norm_dist(rng);
	}
}

int main () {
    // create array with logarithmically distributed values from 10 to 10^6
    std::array<double, 101> Ns;
    for (int i = 0; i < 101; i++) {
        double exponent = 5/100.0f * i + 1;
        Ns[i] = std::pow(10, exponent);
        // THIS LINE CREATES PROBLEMS WITH G++ WITH THE -O3
        std::cout << exponent << std::endl;
    }


    // initialize the random number generator
    std::mt19937 rng(SEED);


    // initialize the file to write to
    std::ofstream file;
    file.open("data.txt");

    // write in the values
    std::vector<double> sample;
    for(double n: Ns) {
        sample.resize(floor(n + 0.5f));
        for (int m = 0; m < 100; m++) {
            fill_vector_with_normal(sample, 0, 1, rng);
            file << measurement_average<double, double>(std::cos, sample);
            if (m < 99) file << ", ";
            else file << "\n";
            std::cout << " Finished N=" << n << " m=" << m << std::endl;
        }
    }
    file.close();
}

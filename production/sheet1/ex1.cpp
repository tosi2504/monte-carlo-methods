#include "statistics.hpp"

#include <vector>
#include <random>
#include <iostream>

void fill_vector_with_normal(std::vector<double> & sample, double mean, double sigma, std::mt19937 & rng) {
	std::normal_distribution<> norm_dist{mean, sigma};
	for (double & val: sample) {
		val = norm_dist(rng);
	}
}

int main () {
	std::mt19937 rng(0);
	std::vector<double> sample;
	sample.resize(1000);
	fill_vector_with_normal(sample, 300, 1, rng);
	double m = mean(sample);
	double s = stdev(sample, m);
	std::cout << "Mean: " << m << std::endl;
	std::cout << "Stdev: " << s << std::endl;
}

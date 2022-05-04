#include "statistics.hpp"
#include <vector>


double mean(const std::vector<double> & data) {
	double res = 0;
	for (double val: data) { // try with &
		res += val;
	}
	return res / data.size();
}

double stdev(const std::vector<double> & data, double mean) {
	double res = 0;
	for (double val: data) {
		res += (val - mean) * (val - mean);
	}
	return res / (data.size() - 1);
}

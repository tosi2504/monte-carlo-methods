#include "core.hpp"
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(pyIsing, m) {
    py::class_<IsingModel>(m, "IsingModel")
        .def(py::init<unsigned int, unsigned int>())
        .def("metropolis_sweep", &IsingModel::metropolis_sweep)
		.def("hmc_one_step", &IsingModel::hmc_one_step)
        .def_readonly("E", &IsingModel::E)
        .def_readonly("M_vec_x", &IsingModel::M_vec_x)
        .def_readonly("M_vec_y", &IsingModel::M_vec_y)
		;
}

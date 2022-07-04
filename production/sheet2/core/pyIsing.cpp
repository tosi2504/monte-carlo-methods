#include "core.hpp"
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(pyIsing, m) {
    py::class_<IsingModel>(m, "IsingModel")
        .def(py::init<unsigned int, unsigned int>())
        .def("init_grid", &IsingModel::init_grid)
        .def("metropolis_one_step", &IsingModel::metropolis_one_step)
        .def("metropolis_sweep", &IsingModel::metropolis_sweep)
        .def("wolff", &IsingModel::wolff)
        .def("at", &IsingModel::at)
        .def("set", &IsingModel::set)
        .def("calc_energy", &IsingModel::calc_energy)
        .def_readonly("E", &IsingModel::E)
        .def_readonly("M", &IsingModel::M);
}

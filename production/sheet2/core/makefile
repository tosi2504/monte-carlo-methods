STD = -Wall -Wextra -Wpedantic -std=c++17
INC_PYB = -I/usr/include/python3.8 -I/home/$(USER)/.local/lib/python3.8/site-packages/pybind11/include


pyIsing: core.o pyIsing.cpp
	$(CXX) $(STD) $(INC_PYB) core.o pyIsing.cpp -o pyIsing.so -shared -fPIC

core.o:	core.cpp
	$(CXX) $(STD) -c core.cpp -o core.o -std=c++17 -fPIC

clean:
	rm core.o pyIsing.so

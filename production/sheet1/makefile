LIB_PATH = ../../lib
CMPLR = clang++
CMPLR_GPP = g++

ex1: ex1.cpp
	$(CMPLR) ex1.cpp -I$(LIB_PATH) $(LIB_PATH)/statistics.o -o ex1

ex2: ex2.cpp
	$(CMPLR_GPP) ex2.cpp -o ex2 -O3

clean:
	rm ex2 ex1

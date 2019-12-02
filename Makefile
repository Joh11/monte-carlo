CXXFLAGS = -std=c++11 -O2

sim: main.o sim.o utils.o config.o
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Cleaning stuff
clean:
	rm -f *.o

cleanall: clean
	rm sim

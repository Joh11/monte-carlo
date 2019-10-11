CXXFLAGS = -std=c++11 -g

sim: main.o sim.o utils.o
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Cleaning stuff
clean:
	rm -f *.o

cleanall: clean
	rm sim

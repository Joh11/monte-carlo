#include <iostream>
#include <random>
#include <algorithm>

#include "sim.hpp"

using namespace std;

int main()
{
    Sim sim{30, 3000, "data/data.out", 200, 1, {0, 0, 10}};

    sim.run();
    
    return 0;
}

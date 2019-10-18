#include <iostream>
#include <random>
#include <algorithm>

#include "config.hpp"
#include "sim.hpp"

using namespace std;

int main(int argc, char *argv[])
{
    Config cfg{argc, argv};
    // 30, 3000, "data/data.out", 200, 1, {0, 0, 10}

    Sim sim{cfg};
    sim.run();

    return 0;
}

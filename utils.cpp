#include <algorithm>
#include <random>
#include <cmath>

#include "utils.hpp"

using namespace std;

mt19937 mte(1730);// Fixed seed for determinism

Vec uniform_on_sphere(size_t dim)
{
    /*
      Generates random normalized vectors. This code uses normal
      distributions, then normalize them to ensure uniformity
      (compared to other methods like normalizing an uniform
      distribution)
     */
    
    normal_distribution<double> ndist;

    Vec vec(3);
    generate(begin(vec), end(vec), [&](){ return ndist(mte); });

    return vec / sqrt(vec * vec).sum();
}

std::valarray<size_t> random_site(size_t N, size_t dim)
{
    uniform_int_distribution<size_t> udist{0, N-1};

    std::valarray<size_t> v(3);
    generate(begin(v), end(v), [&](){return udist(mte); });

    return v;
}

double uniform_unit()
{
    static uniform_real_distribution<double> udist;
    return udist(mte);
}

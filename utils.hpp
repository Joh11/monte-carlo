#ifndef UTILS_HPP
#define UTILS_HPP

#include <valarray>
#include <random>

/*
  Utility file containing both typedefs and random number generation
 */

template <typename T>
using Grid3D = std::valarray<T>;

using Vec = std::valarray<double>;
using Spin = std::valarray<double>;

Vec uniform_on_sphere(size_t dim = 3);
std::valarray<size_t> random_site(size_t N, size_t dim = 3);
double uniform_unit();

// Print operator for valarray
template <typename T>
std::ostream& operator<<(std::ostream& out, std::valarray<T> const& v)
{
    for(size_t i = 0 ; i < v.size() - 1 ; ++i)
    {
	out << v[i] << " ";
    }

    return out << v[v.size() - 1];
}

#endif

#ifndef UTILS_HPP
#define UTILS_HPP

#include <stdexcept>
#include <vector>
#include <valarray>
#include <random>
#include <iostream>

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

template<typename T>
std::string printRaw(std::valarray<T> const& v)
{
    std::string s = "";
    for(size_t i = 0 ; i < v.size() - 1 ; ++i)
    {
	s += std::to_string(v[i]) + " ";
    }

    return s + std::to_string(v[v.size() - 1]);
}

// Print operator for valarray v -> "[v1 v2 v3 ...]"
template <typename T>
std::ostream& operator<<(std::ostream& out, std::valarray<T> const& v)
{
    return out << "(" << printRaw(v) << ")";
}

template <typename T>
std::istream& operator>>(std::istream& in, std::valarray<T> & v)
{
    char c;
    in >> c;
    if(c != '(')
	throw std::runtime_error{"No parenthesis"};

    std::vector<T> vec;
    while(in.good())
    {
	T val;
	in >> val;
	in >> c;
	vec.push_back(val);
	if (c == ')')
	    break;
    }

    v.resize(vec.size());
    std::copy(std::begin(vec), std::end(vec), std::begin(v));

    return in;
}

#endif

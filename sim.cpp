#include <cmath>
#include <iostream>

#include "sim.hpp"
#include "utils.hpp"

using namespace std;

Sim::Sim(size_t N, size_t Nsteps, string const& filename, double temperature, double kb, double J, Vec H)
    : _N{N}, _Nsteps{Nsteps}, _out{filename}, _kbT{temperature * kb}, _J{J}, _H{H}
{
    // Make N^3 spins
    _spins.resize(N * N * N);
    // Generate random starting configuration
    generate(begin(_spins), end(_spins), [](){ return uniform_on_sphere(); });    
}

Sim::Sim(Config const& params) :
    Sim(params.get<double>("N"), params.get<double>("Nsteps")
	, params.get<string>("filename"), params.get<double>("kb") * params.get<double>("temperature")
	, params.get<double>("J"), params.get<Vec>("H")) {}

void Sim::run()
{
    auto oldEnergy = energy();
    auto M = magnetization();

    size_t printIter = _Nsteps / 10;
    
    for(size_t i = 0 ; i < _Nsteps ; ++i)
    {
	if(i % printIter == 0)
	    cout << "iteration " << i << endl;
	
	// Take a random site
        auto rs = random_site(_N);
	// Change its spin
	auto oldSpin = _spins[index(rs)];
	_spins[index(rs)] = uniform_on_sphere();
	// Compute the difference in energy
        auto E = energy();
	auto delta = E - oldEnergy;
	// Accept or not
	if(delta < 0 || uniform_unit() <= exp(- (1.0 / _kbT) * delta))
	{
	    // Accept
	    oldEnergy = E;
	    M = magnetization();
	}
	else
	{
	    // Reject
	    _spins[index(rs)] = oldSpin;
	}

	// Output
	_out << i << " " << E << " " << printRaw(M) << endl;
    }
}

double Sim::energy() const
{
    Vec magnetization{0, 0, 0};
    double interaction = 0;
    
    for(size_t i = 0 ; i < _N ; ++i)
    {
	for(size_t j = 0 ; j < _N ; ++j)
	{
	    for(size_t k = 0 ; k < _N ; ++k)
	    {
		auto const& s = _spins[index(i, j, k)];
		
		// Get half of all the nearest neighbors
		auto const& n1 = _spins[index(i + 1, j, k)];
		auto const& n2 = _spins[index(i, j + 1, k)];
		auto const& n3 = _spins[index(i, j, k + 1)];

		magnetization += s;
		interaction += (n1 * s).sum() + (n2 * s).sum() + (n3 * s).sum();
	    }
	}
    }

    return -_J * interaction - (_H * magnetization).sum();
}

Spin Sim::magnetization() const
{
    return _spins.sum();
}

size_t Sim::index(size_t i, size_t j, size_t k) const
{
    i = i % _N;
    j = j % _N;
    k = k % _N;
    return _N * _N * i + _N * j + k;
}

size_t Sim::index(std::valarray<size_t> v) const
{
    return index(v[0], v[1], v[2]);
}

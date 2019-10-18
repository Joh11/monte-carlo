#ifndef CONFIG_HPP
#define CONFIG_HPP

#include <map>
#include <stdexcept>
#include <string>
#include <sstream>

class Config
{
public:
    Config(int argc, char *argv[]);

    template<typename T>
    T get(std::string const& key) const
    {
	auto it = _map.find(key);
	if(it == std::end(_map))
	    throw std::runtime_error{"No such key found : " + key};

	T val;
	std::istringstream s{it->second};
	s >> val;

	return val;
    }

private:
    bool process(std::string const& str);
    
    std::map<std::string, std::string> _map;
};

#endif

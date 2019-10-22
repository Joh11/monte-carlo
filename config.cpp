#include <fstream>
#include <iostream>

#include "config.hpp"

using namespace std;

Config::Config(int argc, char *argv[])
{
    if(argc <= 1)
        return; // Nothing to parse

    ifstream f{argv[1]};


    // Process the config file first
    std::string line;
    while(getline(f, line))
	process(line);

    // Then the command line arguments
    if(argc >= 2)
    {
        for(size_t i = 2 ; i < argc ; ++i)
            process(argv[i]);
    }

    // Print everything
    for(auto it=_map.begin() ; it != _map.end() ; ++it)
	cout << it->first << " = " << it->second << endl;
}

bool Config::process(std::string const& str)
{
    if(str[0] == '#') // Comments
	return true;
    
    auto eq = str.find('=');

    if(eq == str.npos)
	return false;

    auto key = str.substr(0, eq);
    auto value = str.substr(eq + 1);

    _map[key] = value;

    return true;
}

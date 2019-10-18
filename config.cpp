#include <fstream>
#include <iostream>

#include "config.hpp"

using namespace std;

Config::Config(int argc, char *argv[])
{
    if(argc <= 1)
        return; // Nothing to parse

    ifstream f{argv[1]};
    
    std::string line;
    while(getline(f, line))
	process(line);

    cout << endl << endl;
}

bool Config::process(std::string const& str)
{
    cout << str << endl;
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

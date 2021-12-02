#include <iostream>
#include <fstream>
#include <ctime>
#include <complex>
#include <vector>
#include <sstream>

using namespace std;
using namespace std::complex_literals;

typedef complex<double> Lattice;
struct Command
{
    Lattice direction;
    int units;
};

struct Results
{
    int part1;
    int part2;
};
typedef vector<Command> Input;

int part1(Input commands)
{
    Lattice position = 0;
    for (auto &command: commands)
        position += command.direction * (Lattice)command.units;
    return (int)(position.real() * position.imag());
}

int part2(Input commands)
{
    Lattice position = 0;
    Lattice aim = 0;
    for (auto &command: commands)
        if (command.direction == (Lattice)1)
            position += (Lattice)command.units * ((Lattice)1 + aim);
        else
            aim += command.direction * (Lattice)command.units;
    return (int)(position.real() * position.imag());
}

Results solve(Input puzzleInput)
{
    return {part1(puzzleInput), part2(puzzleInput)};
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    string line, command;
    int units;
    Lattice direction;
    Input commands;
    while (getline(file, line))
    {
        stringstream ss(line);
        ss >> command;
        ss >> units;
        if (command == "forward")
            direction = 1;
        else if (command == "down")
            direction = 1i;
        else if (command == "up")
            direction = -1i;
        else
            throw runtime_error("Unknow command");
        commands.push_back({direction, units});
    }
    file.close();
    return commands;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
        throw runtime_error("Please, add input file path as parameter");

    clock_t begin = clock();
    auto results = solve(getInput(argv[1]));
    clock_t end = clock();
    auto elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    cout << "P1: " << results.part1 << endl;
    cout << "P2: " << results.part2 << endl;
    cout << endl;
    cout.precision(7);
    cout << "Time: " << std::fixed << elapsed_secs << endl;
    return 0;
}

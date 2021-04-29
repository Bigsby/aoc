#include <iostream>
#include <fstream>
#include <ctime>
#include <regex>
#include <vector>
#include <complex>
#include <cmath>

using namespace std;
using namespace std::complex_literals;

struct Results
{
    int part1;
    int part2;
};

struct Instruction
{
    char direction;
    int distance;
    Instruction(char dir, int dis)
    {
        direction = dir;
        distance = dis;
    }
};

int getManhatanDistance(complex<double> position)
{
    return abs<double>(position.real()) + abs<double>(position.imag());
}

Results solve(vector<Instruction> instructions)
{
    complex<double> position;
    complex<double> heading = 1i;
    int part2 = 0;
    vector<complex<double>> visited;
    for (Instruction instruction : instructions)
    {
        heading *= instruction.direction == 'L' ? 1i : -1i;
        for (auto i = 0; i < instruction.distance; i++)
        {
            position += heading;
            if (part2 == 0)
            {
                if (find(visited.begin(), visited.end(), position) != visited.end())
                {
                    part2 = getManhatanDistance(position);
                }
                else
                {
                    visited.push_back(position);
                }
            }
        }
    }
    return {getManhatanDistance(position), part2};
}

vector<Instruction> getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    string content((istreambuf_iterator<char>(file)), (istreambuf_iterator<char>()));
    file.close();
    regex instructions_regex("([RL])(\\d+),?\\s?");
    vector<Instruction> instructions;
    for (sregex_iterator i = sregex_iterator(content.begin(), content.end(), instructions_regex);
         i != sregex_iterator(); i++)
    {
        smatch match = *i;
        instructions.push_back(Instruction(match.str(1)[0], stoi(match.str(2))));
    }
    return instructions;
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
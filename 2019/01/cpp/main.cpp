#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <algorithm>
#include <numeric>

using namespace std;

struct Results
{
    int part1;
    int part2;
};
typedef vector<int> Input;

int part2(int mass)
{
    int total = 0;
    int currentMass = mass;
    while (1)
    {
        int fuel = currentMass / 3 - 2;
        if (fuel <= 0)
            return total;
        total += fuel;
        currentMass = fuel;
    }
}

int getTotalFuel(Input masses, int (*fuelCalculator)(int))
{
    int total = 0;
    for (auto mass : masses)
        total += fuelCalculator(mass);
    return total;
}

Results solve(Input masses)
{
    return {getTotalFuel(masses, [](int mass) { return mass / 3 - 2; }), getTotalFuel(masses, &part2)};
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");
    string line;
    vector<int> masses;
    while (getline(file, line))
        masses.push_back(stoi(line));
    file.close();
    return masses;
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
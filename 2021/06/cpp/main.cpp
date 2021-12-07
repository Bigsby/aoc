#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <algorithm>
#include <numeric>

using namespace std;

struct Results
{
    unsigned long part1;
    unsigned long part2;
};
typedef vector<int> Input;

unsigned long runGenerations(Input fishes, int generations)
{
    unsigned long  fishCounts[9] = {0};
    for (auto fish: fishes)
        fishCounts[fish]++;
    while (generations--)
    {
        auto fishesAtZero = fishCounts[0];
        for (auto day = 0; day < 8; day++)
            fishCounts[day] = fishCounts[day + 1];
        fishCounts[8] = fishesAtZero;
        fishCounts[6] += fishesAtZero;
    }
    return accumulate(fishCounts, fishCounts + 9, 0UL);
}

Results solve(Input puzzleInput)
{
    return {runGenerations(puzzleInput, 80), runGenerations(puzzleInput, 256)};
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    string fish;
    vector<int> fishes;
    while (getline(file, fish, ','))
        fishes.push_back(stoi(fish));
        
    file.close();
    return fishes;
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

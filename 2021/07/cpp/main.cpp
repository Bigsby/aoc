#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>

using namespace std;

struct Results
{
    int part1;
    int part2;
};
typedef vector<int> Input;

int part1(Input crabs)
{
    sort(crabs.begin(), crabs.end());
    int mean = crabs[crabs.size() / 2];
    return accumulate(crabs.begin(), crabs.end(), 0, [mean](int soFar, int crab){ return abs(crab - mean) + soFar; });
}

int getDistanceCost(int posA, int posB)
{
    int distance = abs(posA - posB);
    return (distance * (distance + 1)) / 2;
}

int part2(Input crabs)
{
    int average = accumulate(crabs.begin(), crabs.end(), 0) / crabs.size();
    return accumulate(crabs.begin(), crabs.end(), 0, [average](int soFar, int crab) { return soFar + getDistanceCost(average, crab); });
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

    string crab;
    vector<int> crabs;
    while (getline(file, crab, ','))
        crabs.push_back(stoi(crab));
        
    file.close();
    return crabs;
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

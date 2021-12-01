#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <limits>

using namespace std;

struct Results
{
    int part1;
    int part2;
};
typedef vector<int> Input;

int part1(Input depths)
{
    int increments = 0;
    int lastDepth = numeric_limits<int>::max();
    for (auto depth: depths)
    {
        increments += depth > lastDepth;
        lastDepth = depth;
    }
    return increments;
}

int part2(Input depths)
{
    int increments = 0;
    int lastDepth = numeric_limits<int>::max();
    for (auto index = 0; index < depths.size(); index++)
    {
        int depth = depths[index] + depths[index + 1] + depths[index + 2];
        increments += depth > lastDepth;
        lastDepth = depth;
    }
    return increments;
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

    Input input;
    string line;
    while (getline(file, line))
        input.push_back(stoi(line));
    file.close();
    return input;
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

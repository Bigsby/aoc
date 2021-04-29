#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <numeric>
#include <unordered_set>

using namespace std;

int part2(vector<int> changes)
{
    int changes_length = changes.size();
    int frequency = 0;
    unordered_set<int> previous;
    int index = 0;
    while (previous.find(frequency) == previous.end())
    {
        previous.insert(frequency);
        frequency += changes[index];
        index = (index + 1) % changes_length;
    }
    return frequency;
}

struct Results
{
    int part1;
    int part2;
    Results(int p1, int p2)
    {
        part1 = p1;
        part2 = p2;
    }
};

Results solve(vector<int> changes)
{
    int sum;
    return Results(std::accumulate(changes.begin(), changes.end(), 0), part2(changes));
}

vector<int> getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");
    string line;
    vector<int> changes;
    while (getline(file, line))
        changes.push_back(stoi(line));
    file.close();
    return changes;
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
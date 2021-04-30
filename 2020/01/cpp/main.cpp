#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <numeric>
#include <algorithm>

using namespace std;

struct Results
{
    int part1;
    int part2;
};
typedef vector<int> Input;

int getCombination(Input numbers, int length)
{
    int i;
    vector<int> combination(length);
    vector<int> indexes(length);
    for (i = 0; i < length; i++)
        indexes[i] = length - i;
    while (true)
    {
        for (i = length; i--;)
            combination[i] = numbers[indexes[i] - 1];
        if (accumulate(begin(combination), end(combination), 0) == 2020)
            return accumulate(begin(combination), end(combination), 1, multiplies<int>());
        i = 0;
        if (indexes[i]++ < numbers.size())
            continue;
        for (; indexes[i] >= numbers.size() - i;)
            if (++i >= length)
                return 0;
        for (indexes[i]++; i; i--)
            indexes[i - 1] = indexes[i] + 1;
    }
}

Results solve(Input numbers)
{
    return {
        getCombination(numbers, 2),
        getCombination(numbers, 3)};
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");
    string line;
    vector<int> numbers;
    while (getline(file, line))
        numbers.push_back(stoi(line));
    file.close();
    return numbers;
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
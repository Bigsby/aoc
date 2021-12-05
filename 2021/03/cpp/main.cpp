#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <algorithm>

using namespace std;

struct Results
{
    int part1;
    int part2;
};
typedef struct {
    int bitLength;
    vector<int> numbers;
} Input;

int getNthBit1Count(const vector<int> &numbers, int index)
{
    auto mask = 1 << index;
    return count_if(numbers.begin(), numbers.end(), [mask](int number) { return (number & mask) == mask; });
}

int part1(Input puzzleInput)
{
    int gamma = 0, epsilon = 0, half = puzzleInput.numbers.size() / 2;
    for (auto index = puzzleInput.bitLength - 1; index >= 0; index--)
    {
        auto onesCount = getNthBit1Count(puzzleInput.numbers, index);
        gamma = (gamma << 1) + (onesCount > half);
        epsilon = (epsilon << 1) + (onesCount < half);
    }
    return gamma * epsilon;
}

void processBit(vector<int> &numbers, int index, bool mostCommon)
{
    if (numbers.size() == 1)
        return;
    auto onesCount = getNthBit1Count(numbers, index);
    auto zerosCount = numbers.size() - onesCount;
    auto mask = 1 << index;
    auto match = mostCommon ^ (onesCount < zerosCount) ? mask : 0;
    numbers.erase(remove_if(numbers.begin(), numbers.end(), [mask, match](int number) { return (number & mask) == match; }), numbers.end());
}

int part2(Input puzzleInput)
{
    auto oxygen = puzzleInput.numbers;
    auto co2 = puzzleInput.numbers;
    auto index = puzzleInput.bitLength - 1;
    while (oxygen.size() > 1 || co2.size() > 1)
    {
        processBit(oxygen, index, true);
        processBit(co2, index, false);
        index--;
    }
    return oxygen[0] * co2[0];
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
    input.bitLength = 0;
    string line;
    while (getline(file, line))
    {
        if (!input.bitLength)
            input.bitLength = line.length();
        input.numbers.push_back(stoi(line, NULL, 2));
    }
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

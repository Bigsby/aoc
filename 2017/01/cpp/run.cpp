#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>

using namespace std;

int getCount(vector<int> numbers, int indexOffset)
{
    int count = 0;
    for (auto index = 0; index < numbers.size(); index++)
        if (numbers.at(index) == numbers.at((index + indexOffset) % numbers.size()))
            count += numbers.at(index);
    return count;
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

Results solve(vector<int> numbers)
{
    return Results(
        getCount(numbers, numbers.size() - 1),
        getCount(numbers, numbers.size() / 2));
}

vector<int> getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    vector<int> numbers;
    string content((istreambuf_iterator<char>(file)), (istreambuf_iterator<char>()));
    file.close();
    for (char c : content)
        numbers.push_back((int)c - 48);
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
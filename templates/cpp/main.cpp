#include <iostream>
#include <fstream>
#include <ctime>

using namespace std;

struct Results
{
    int part1;
    int part2;
};

int part1(string puzzleInput)
{
    return puzzleInput.length();
}

int part2(string puzzleInput)
{
    return puzzleInput.length();
}

Results solve(string puzzleInput)
{
    return {part1(puzzleInput), part2(puzzleInput)};
}

string getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    string content((istreambuf_iterator<char>(file)), (istreambuf_iterator<char>()));
    file.close();
    return content;
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
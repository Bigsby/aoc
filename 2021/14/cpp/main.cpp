#include <iostream>
#include <fstream>
#include <ctime>
#include <map>
#include <utility>

using namespace std;

struct Results
{
    unsigned long part1;
    unsigned long part2;
};
struct Input {
    string polymer;
    map<pair<char,char>,char> rules;
};

unsigned long runInsertions(Input input, int steps)
{
    map<pair<char,char>,unsigned long> pairOccurrences;
    for (int index = 0; index < input.polymer.length() - 1; index++)
    {
        auto letterPair = make_pair(input.polymer[index], input.polymer[index + 1]);
        if (pairOccurrences.count(letterPair))
            pairOccurrences[letterPair]++;
        else
            pairOccurrences[letterPair] = 1;
    }
    while (steps--)
    {
        map<pair<char,char>,unsigned long> newPairOccurrences;
        for (auto keyValue: pairOccurrences)
        {
            char first = keyValue.first.first;
            char second = keyValue.first.second;
            char newLetter = input.rules[keyValue.first];
            auto firstNewPair = make_pair(first, newLetter);
            auto secondNewPair = make_pair(newLetter, second);
            if (newPairOccurrences.count(firstNewPair))
                newPairOccurrences[firstNewPair] += keyValue.second;
            else
                newPairOccurrences[firstNewPair] = keyValue.second;
            if (newPairOccurrences.count(secondNewPair))
                newPairOccurrences[secondNewPair] += keyValue.second;
            else
                newPairOccurrences[secondNewPair] = keyValue.second;
        }
        pairOccurrences = newPairOccurrences;
    }
    map<char, unsigned long> letterOccurrences;
    for (auto keyValue: pairOccurrences)
        if (letterOccurrences.count(keyValue.first.second))
            letterOccurrences[keyValue.first.second] += keyValue.second;
        else
            letterOccurrences[keyValue.first.second] = keyValue.second;
    letterOccurrences[input.polymer[0]]++;
    unsigned long max = 0;
    unsigned long min = letterOccurrences[input.polymer[0]];
    for (auto keyValue: letterOccurrences)
    {
        max = keyValue.second > max ? keyValue.second : max;
        min = keyValue.second < min ? keyValue.second : min;
    }
    return max - min;
}

Results solve(Input puzzleInput)
{
    return {runInsertions(puzzleInput, 10), runInsertions(puzzleInput, 40)};
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    Input input;
    string line;
    getline(file, line);
    input.polymer = line;
    getline(file, line);
    while (getline(file, line))
        input.rules[make_pair(line[0], line[1])] = line[6];
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

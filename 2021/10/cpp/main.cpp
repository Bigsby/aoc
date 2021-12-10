#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <stack>
#include <map>
#include <algorithm>

using namespace std;

struct Results
{
    int part1;
    unsigned long part2;
};
typedef vector<string> Input;

map<char, char> MATCHES = {
    { '(', ')' },
    { '[', ']' },
    { '{', '}' },
    { '<', '>' }
};

map<char, int> ILLEGAL_CLOSING = {
    { ')', 3 },
    { ']', 57 },
    { '}', 1197 },
    { '>', 25137 }
};

map<char, unsigned long> CLOSING = {
    { ')', 1 },
    { ']', 2 },
    { '}', 3 },
    { '>', 4 }
};

Results solve(Input lines)
{
    vector<unsigned long> incompletePoints;
    int illegalPoints = 0;
    for (auto line: lines)
    {
        stack<char> expectedClosing;
        auto illegal = false;
        for (auto index = 0; index < line.length(); index ++)
        {
            auto c = line[index];
            if (c == '(' || c == '[' || c == '{' || c == '<')
                expectedClosing.push(MATCHES[c]);
            else
            {
                char expected = expectedClosing.top();
                expectedClosing.pop();
                if (c != expected)
                {
                    illegal = true;
                    illegalPoints += ILLEGAL_CLOSING[c];
                    break;
                }
            }
        }
        if (!illegal)
        {
            unsigned long points = 0;
            while (!expectedClosing.empty())
            {
                points = points * 5 + CLOSING[expectedClosing.top()];
                expectedClosing.pop();
            }
            incompletePoints.push_back(points);
        }
    }
    sort(incompletePoints.begin(), incompletePoints.end());
    return {illegalPoints, incompletePoints[incompletePoints.size() / 2]};
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    Input input;
    string line;
    while (getline(file, line))
        input.push_back(line);
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

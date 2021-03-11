#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>

using namespace std;

int part1(vector<int> directions)
{
    int total = 0;
    for (int direction : directions)
        total += direction;
    return total;
}

int part2(vector<int> directions)
{
    int currentFloor = 0;
    for (auto index = 0; index < directions.size(); index++)
    {
        currentFloor += directions[index];
        if (currentFloor == -1)
            return index + 1;
    }
    throw runtime_error("Did not go below 0!");
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

Results solve(vector<int> directions)
{
    return Results(part1(directions), part2(directions));
}

vector<int> getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    string content((istreambuf_iterator<char>(file)), (istreambuf_iterator<char>()));
    vector<int> directions;
    for (char c : content)
    {
        switch (c)
        {
        case '(':
            directions.push_back(1);
            break;
        case ')':
            directions.push_back(-1);
            break;
        }
    }
    file.close();
    return directions;
}


int main(int argc, char *argv[]) {
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
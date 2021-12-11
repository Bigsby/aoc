#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <stack>

using namespace std;

struct Results
{
    int part1;
    int part2;
};
typedef vector<vector<char>> Input;

struct Lattice {
    int x, y;
};

vector<Lattice> getNeighbors(int x, int y)
{
    vector<Lattice> neighbors;
    if (x)
    {
        neighbors.push_back((Lattice){ x - 1, y });
        if (y)
            neighbors.push_back((Lattice){ x - 1, y - 1 });
        if (y < 9)
            neighbors.push_back((Lattice){ x - 1, y + 1 });
    }
    if (x < 9)
    {
        neighbors.push_back((Lattice){ x + 1, y });
        if (y)
            neighbors.push_back((Lattice){ x + 1, y - 1 });
        if (y < 9)
            neighbors.push_back((Lattice){ x + 1, y + 1 });
    }
    if (y)
        neighbors.push_back((Lattice){ x, y - 1 });
    if (y < 9)
        neighbors.push_back((Lattice){ x, y + 1 });
    return neighbors;
}

Results solve(Input octopuses)
{
    int flashes = 0;
    int allFlashes = 0;
    int step = 0;
    while (!allFlashes || step <= 100)
    {
        step++;
        int stepFlashes = 0;
        stack<Lattice> toProcess;
        for (auto y = 0; y < 10; y++)
            for (auto x = 0; x < 10; x++)
            {
                octopuses[y][x]++;
                if (octopuses[y][x] == 10)
                    toProcess.push((Lattice){ x, y });
            }
        while (!toProcess.empty())
        {
            Lattice octopus = toProcess.top();
            toProcess.pop();
            if (octopuses[octopus.y][octopus.x] == 0)
                continue;
            stepFlashes++;
            octopuses[octopus.y][octopus.x] = 0;
            for (auto neighbor: getNeighbors(octopus.x, octopus.y))
            {
                if (octopuses[neighbor.y][neighbor.x] == 0)
                    continue;
                octopuses[neighbor.y][neighbor.x]++;
                if (octopuses[neighbor.y][neighbor.x] == 10)
                    toProcess.push((Lattice){ neighbor.x, neighbor.y });
            }
        }
        if (step <= 100)
            flashes += stepFlashes;
        if (stepFlashes == 100)
            allFlashes = step;
    }
    return {flashes, allFlashes};
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    string line;
    Input input;
    while (getline(file, line))
    {
        vector<char> row;
        for (auto index = 0; index < line.length(); index++)
            row.push_back(line[index] - '0');
        input.push_back(row);
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

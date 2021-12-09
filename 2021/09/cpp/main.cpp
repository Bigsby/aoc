#include <iostream>
#include <fstream>
#include <ctime>
#include <complex>
#include <map>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

struct Results
{
    int part1;
    int part2;
};
typedef complex<double> Lattice;

struct LatticeComparator {
    Lattice match;
    LatticeComparator() {}
    LatticeComparator(Lattice const &position): match(position) { }

    bool operator()(Lattice const &position)
    {
        return position == match;
    }

    bool operator()(const Lattice &a, const Lattice &b) const
    {
        if (a.real() < b.real())
            return true;
        if (a.real() > b.real())
            return false;
        return a.imag() < b.imag();
    }
};
typedef map<Lattice, int, LatticeComparator> LatticeMap;
struct Input {
    LatticeMap heightMap;
    int maxX, maxY;
};

vector<Lattice> getNeighbors(int maxX, int maxY, Lattice position)
{
    vector<Lattice> neighbors;
    if (position.real())
        neighbors.push_back(Lattice(position.real() - 1, position.imag()));
    if (position.imag())
        neighbors.push_back(Lattice(position.real(), position.imag() - 1));
    if (position.real() < maxX - 1)
        neighbors.push_back(Lattice(position.real() + 1, position.imag()));
    if (position.imag() < maxY - 1)
        neighbors.push_back(Lattice(position.real(), position.imag() + 1));
    return neighbors;
}

int getPositionRisk(Input input, Lattice position)
{
    auto height = input.heightMap[position];
    for (auto neighbor: getNeighbors(input.maxX, input.maxY, position))
        if (input.heightMap[neighbor] <= height)
            return 0;
    return height + 1;
}

bool visitedContains(vector<Lattice> visited, Lattice position)
{
    return find_if(visited.begin(), visited.end(), LatticeComparator(position)) != visited.end();
}

int getBasinSize(Input input, Lattice position)
{
    queue<Lattice> toVisit;
    vector<Lattice> visited;
    toVisit.push(position);
    while (!toVisit.empty())
    {
        auto current = toVisit.front();
        toVisit.pop();
        if (visitedContains(visited, current))
            continue;
        auto currentHeight = input.heightMap[current];
        visited.push_back(current);
        for (auto neighbor: getNeighbors(input.maxX, input.maxY, current))
        {
            auto neighborHeight = input.heightMap[neighbor];
            if (neighborHeight == 9 || neighborHeight <= currentHeight || visitedContains(visited, neighbor))
                continue;
            toVisit.push(neighbor);
        }
    }
    return visited.size();
}

void addToSizes(int *sizes, int size)
{
    for (int index = 0; index < 3; index++)
        if (size >= sizes[index])
        {
            int oldSize = sizes[index];
            sizes[index] = size;
            size = oldSize;
        }
}

Results solve(Input puzzleInput)
{
    auto lowestSum = 0;
    int sizes[3] = { 0 };
    for (auto y = 0; y < puzzleInput.maxY; y++)
        for (auto x = 0; x < puzzleInput.maxX; x++)
        {
            auto position = Lattice(x, y);
            auto positionRisk = getPositionRisk(puzzleInput, position);
            if (positionRisk)
            {
                lowestSum += positionRisk;
                addToSizes(sizes, getBasinSize(puzzleInput, position));
            }
        }
    return { lowestSum, sizes[0] * sizes[1] * sizes[2] };
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    Input input;
    string line;
    Lattice position = 0;
    while (getline(file, line))
    {
        for (auto c: line)
        {
            
            if (c == '\n')
                continue;
            input.heightMap[position] = c - '0';
            position += 1;
        }
        input.maxX = position.real();
        position = Lattice(0, position.imag() + 1);
    }
    input.maxY = position.imag();
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

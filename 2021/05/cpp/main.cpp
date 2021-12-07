#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <regex>
#include <map>
#include <cmath>

using namespace std;

struct Results
{
    int part1;
    int part2;
};
struct Line {
    int x1, y1, x2, y2;
};
typedef vector<Line> Input;

struct Point {
    int x, y;
};

int getCoveredPoints(Input lines, const bool diagonals)
{
    auto comparePoints = [](const Point &a, const Point &b) {
        if (a.x < b.x)
            return true;
        if (a.x > b.x)
            return false;
        return a.y < b.y;
    };
    map<Point,int,decltype(comparePoints)> diagram(comparePoints);
    auto addToDiagram = [&diagram](const Point point) { if (diagram.count(point)) diagram[point]++; else diagram[point] = 1; };
    for (auto line: lines)
    {
        if (line.x1 == line.x2)
            for (auto y = line.y1 < line.y2 ? line.y1 : line.y2; y < (line.y1 > line.y2 ? line.y1 : line.y2) + 1; y++)
                addToDiagram(Point { line.x1, y });
        else if (line.y1 == line.y2)
            for (auto x = line.x1 < line.x2 ? line.x1 : line.x2; x < (line.x1 > line.x2 ? line.x1 : line.x2) + 1; x++)
                addToDiagram(Point { x, line.y1 });
        else if (diagonals)
        {
            int xDirection = line.x2 > line.x1 ? 1 : -1;
            int yDirection = line.y2 > line.y1 ? 1 : -1;
            int count = abs(line.x2 - line.x1);
            for (auto xy = 0; xy <= count; xy++)
                addToDiagram(Point { line.x1 + xy * xDirection, line.y1 + xy * yDirection });
        }
    }
    int total = 0;
    for (const auto &pair: diagram)
        if (pair.second > 1)
            total++;
    return total;
}

Results solve(Input lines)
{
    return {getCoveredPoints(lines, false), getCoveredPoints(lines, true)};
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    vector<Line> lines;
    string line;
    regex lineRegex("(\\d+),(\\d+) -> (\\d+),(\\d+)");
    while (getline(file, line))
    {
        smatch lineMatch;
        if (regex_match(line, lineMatch, lineRegex))
            lines.push_back(Line {
                stoi(lineMatch.str(1)),
                stoi(lineMatch.str(2)),
                stoi(lineMatch.str(3)),
                stoi(lineMatch.str(4))
            });
        else
            throw runtime_error("Bad line.");

    }
    file.close();
    return lines;
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

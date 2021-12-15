#include <iostream>
#include <fstream>
#include <ctime>
#include <complex>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>

using namespace std;
using namespace std::complex_literals;

typedef complex<double> Point;
struct Folding {
    bool xDirection;
    int coordinate;
    Folding(bool direction, int coordinate): xDirection(direction), coordinate(coordinate)
    { }
};
struct Results
{
    int part1;
    string part2;
};
struct Input { 
    vector<Point> points;
    vector<Folding> foldings;
};

#define SCREEN_WIDTH 40
#define SCREEN_HEIGHT 6
#define CHARACTER_WIDTH 5

map<int, char> LETTERS = {
    {   (0b01100 << CHARACTER_WIDTH * 0) +
        (0b10010 << CHARACTER_WIDTH * 1) +
        (0b10010 << CHARACTER_WIDTH * 2) +
        (0b11110 << CHARACTER_WIDTH * 3) +
        (0b10010 << CHARACTER_WIDTH * 4) +
        (0b10010 << CHARACTER_WIDTH * 5), 'A' },

    {   (0b11100 << CHARACTER_WIDTH * 0) +
        (0b10010 << CHARACTER_WIDTH * 1) +
        (0b11100 << CHARACTER_WIDTH * 2) +
        (0b10010 << CHARACTER_WIDTH * 3) +
        (0b10010 << CHARACTER_WIDTH * 4) +
        (0b11100 << CHARACTER_WIDTH * 5), 'B' },

    {   (0b01100 << CHARACTER_WIDTH * 0) +
        (0b10010 << CHARACTER_WIDTH * 1) +
        (0b10000 << CHARACTER_WIDTH * 2) +
        (0b10000 << CHARACTER_WIDTH * 3) +
        (0b10010 << CHARACTER_WIDTH * 4) +
        (0b01100 << CHARACTER_WIDTH * 5), 'C' },

    {   (0b11100 << CHARACTER_WIDTH * 0) +
        (0b10010 << CHARACTER_WIDTH * 1) +
        (0b10010 << CHARACTER_WIDTH * 2) +
        (0b10010 << CHARACTER_WIDTH * 3) +
        (0b10010 << CHARACTER_WIDTH * 4) +
        (0b11100 << CHARACTER_WIDTH * 5), 'D' },

    {   (0b11110 << CHARACTER_WIDTH * 0) +
        (0b10000 << CHARACTER_WIDTH * 1) +
        (0b11100 << CHARACTER_WIDTH * 2) +
        (0b10000 << CHARACTER_WIDTH * 3) +
        (0b10000 << CHARACTER_WIDTH * 4) +
        (0b11110 << CHARACTER_WIDTH * 5), 'E' },

    {   (0b11110 << CHARACTER_WIDTH * 0) +
        (0b10000 << CHARACTER_WIDTH * 1) +
        (0b11100 << CHARACTER_WIDTH * 2) +
        (0b10000 << CHARACTER_WIDTH * 3) +
        (0b10000 << CHARACTER_WIDTH * 4) +
        (0b10000 << CHARACTER_WIDTH * 5), 'F' },

    {   (0b01100 << CHARACTER_WIDTH * 0) +
        (0b10010 << CHARACTER_WIDTH * 1) +
        (0b10000 << CHARACTER_WIDTH * 2) +
        (0b10110 << CHARACTER_WIDTH * 3) +
        (0b10010 << CHARACTER_WIDTH * 4) +
        (0b01110 << CHARACTER_WIDTH * 5), 'G' },

    {   (0b10010 << CHARACTER_WIDTH * 0) +
        (0b10010 << CHARACTER_WIDTH * 1) +
        (0b11110 << CHARACTER_WIDTH * 2) +
        (0b10010 << CHARACTER_WIDTH * 3) +
        (0b10010 << CHARACTER_WIDTH * 4) +
        (0b10010 << CHARACTER_WIDTH * 5), 'H' },

    {   (0b01110 << CHARACTER_WIDTH * 0) +
        (0b00100 << CHARACTER_WIDTH * 1) +
        (0b00100 << CHARACTER_WIDTH * 2) +
        (0b00100 << CHARACTER_WIDTH * 3) +
        (0b00100 << CHARACTER_WIDTH * 4) +
        (0b01110 << CHARACTER_WIDTH * 5), 'I' },

    {   (0b00110 << CHARACTER_WIDTH * 0) +
        (0b00010 << CHARACTER_WIDTH * 1) +
        (0b00010 << CHARACTER_WIDTH * 2) +
        (0b00010 << CHARACTER_WIDTH * 3) +
        (0b10010 << CHARACTER_WIDTH * 4) +
        (0b01100 << CHARACTER_WIDTH * 5), 'J' },

    {   (0b10010 << CHARACTER_WIDTH * 0) +
        (0b10100 << CHARACTER_WIDTH * 1) +
        (0b11000 << CHARACTER_WIDTH * 2) +
        (0b10100 << CHARACTER_WIDTH * 3) +
        (0b10100 << CHARACTER_WIDTH * 4) +
        (0b10010 << CHARACTER_WIDTH * 5), 'K' },

    {   (0b10000 << CHARACTER_WIDTH * 0) +
        (0b10000 << CHARACTER_WIDTH * 1) +
        (0b10000 << CHARACTER_WIDTH * 2) +
        (0b10000 << CHARACTER_WIDTH * 3) +
        (0b10000 << CHARACTER_WIDTH * 4) +
        (0b11110 << CHARACTER_WIDTH * 5), 'L' },

    {   (0b01100 << CHARACTER_WIDTH * 0) +
        (0b10010 << CHARACTER_WIDTH * 1) +
        (0b10010 << CHARACTER_WIDTH * 2) +
        (0b10010 << CHARACTER_WIDTH * 3) +
        (0b10010 << CHARACTER_WIDTH * 4) +
        (0b01100 << CHARACTER_WIDTH * 5), 'O' },

    {   (0b11100 << CHARACTER_WIDTH * 0) +
        (0b10010 << CHARACTER_WIDTH * 1) +
        (0b10010 << CHARACTER_WIDTH * 2) +
        (0b11100 << CHARACTER_WIDTH * 3) +
        (0b10000 << CHARACTER_WIDTH * 4) +
        (0b10000 << CHARACTER_WIDTH * 5), 'P' },

    {   (0b11100 << CHARACTER_WIDTH * 0) +
        (0b10010 << CHARACTER_WIDTH * 1) +
        (0b10010 << CHARACTER_WIDTH * 2) +
        (0b11100 << CHARACTER_WIDTH * 3) +
        (0b10100 << CHARACTER_WIDTH * 4) +
        (0b10010 << CHARACTER_WIDTH * 5), 'R' },

    {   (0b01110 << CHARACTER_WIDTH * 0) +
        (0b10000 << CHARACTER_WIDTH * 1) +
        (0b10000 << CHARACTER_WIDTH * 2) +
        (0b01100 << CHARACTER_WIDTH * 3) +
        (0b00010 << CHARACTER_WIDTH * 4) +
        (0b11100 << CHARACTER_WIDTH * 5), 'S' },

    {   (0b10010 << CHARACTER_WIDTH * 0) +
        (0b10010 << CHARACTER_WIDTH * 1) +
        (0b10010 << CHARACTER_WIDTH * 2) +
        (0b10010 << CHARACTER_WIDTH * 3) +
        (0b10010 << CHARACTER_WIDTH * 4) +
        (0b01100 << CHARACTER_WIDTH * 5), 'U' },

    {   (0b10001 << CHARACTER_WIDTH * 0) +
        (0b10001 << CHARACTER_WIDTH * 1) +
        (0b01010 << CHARACTER_WIDTH * 2) +
        (0b00100 << CHARACTER_WIDTH * 3) +
        (0b00100 << CHARACTER_WIDTH * 4) +
        (0b00100 << CHARACTER_WIDTH * 5), 'Y' },

    {   (0b11110 << CHARACTER_WIDTH * 0) +
        (0b00010 << CHARACTER_WIDTH * 1) +
        (0b00100 << CHARACTER_WIDTH * 2) +
        (0b01000 << CHARACTER_WIDTH * 3) +
        (0b10000 << CHARACTER_WIDTH * 4) +
        (0b11110 << CHARACTER_WIDTH * 5), 'Z' }
};

bool pointsContain(vector<Point> points, Point point)
{
    return count(points.begin(), points.end(), point) != 0;
}

Point createPoint(int x, int y)
{
    return (double)x + (double)y * 1i;
}

char getCharacterInPaper(vector<Point> points, int index, int width, int height)
{
    int paperValue = 0;
    int x, y;
    for (x = 0; x < width; x++)
        for (y = 0; y < height; y++)
            paperValue += pointsContain(points, createPoint(width * index + x, y)) * (int)pow(2, width - 1 - x) << (y * width);
    return LETTERS[paperValue];
}


vector<Point> fold(vector<Point> points, Folding folding)
{
    auto includeFunc = folding.xDirection ?
        [](Point point) { return point.real(); }
        :
        [](Point point) { return point.imag(); };
    auto newPointFunc = folding.xDirection ?
        [](Point point, int coordinate) { return 2 * coordinate - point.real() + point.imag() * 1i; }
        :
        [](Point point, int coordinate) { return point.real() + (2 * coordinate - point.imag()) * 1i; };
    vector<Point> newPoints;
    for (auto point: points)
    {
        auto newPoint = includeFunc(point) < folding.coordinate ? point : newPointFunc(point, folding.coordinate);
        if (!count(newPoints.begin(), newPoints.end(), newPoint))
            newPoints.push_back(newPoint);
    }
    return newPoints;
}

Results solve(Input puzzleInput)
{
    int part1 = 0;
    auto points = puzzleInput.points;
    for (auto folding: puzzleInput.foldings)
    {
        points = fold(points, folding);
        if (!part1)
            part1 = points.size();
    }
    string code = "";
    for (int index = 0; index < SCREEN_WIDTH / CHARACTER_WIDTH; index++)
        code.push_back(getCharacterInPaper(points, index, CHARACTER_WIDTH, SCREEN_HEIGHT));
    return {part1, code};
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    Input input;
    string line;
    bool foldings = false;
    double x, y;
    string value;
    while (getline(file, line))
    {
        if (line.empty())
        {
            foldings = true;
            continue;
        }
        if (foldings)
        {
            input.foldings.push_back(Folding(
                line[11] == 'x',
                stoi(line.substr(line.find("=") + 1))
            ));
        }
        else
        {
            istringstream ss(line);
            getline(ss, value, ',');
            x = stod(value);
            getline(ss, value, ',');
            y = stod(value);
            input.points.push_back(x + y * 1i);
        }
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

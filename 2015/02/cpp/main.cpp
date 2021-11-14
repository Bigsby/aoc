#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <regex>

using namespace std;

struct Results
{
    int part1;
    int part2;
};

struct Dimension {
    int width, length, height;
};

typedef vector<Dimension> Input;

int part1(Input dimensions)
{
    int totalPaper = 0, wl, wh, lh, smallest;
    for (auto dimension : dimensions)
    {
        wl = dimension.width * dimension.length;
        wh = dimension.width * dimension.height;
        lh = dimension.length * dimension.height;
        smallest = min({wl, wh, lh});
        totalPaper += 2 * (wl + wh + lh) + smallest;
    }
    return totalPaper;
}

int part2(Input dimensions)
{
    int totalRibbon = 0; 
    int height, length, width;
    int smaller1, smaller2, intermediate;
    for (auto dimension: dimensions)
    {
        height = dimension.height;
        length = dimension.length;
        width = dimension.width;
        if (height > length)
        {
            smaller1 = length;
            intermediate = height;
        }
        else
        {
            smaller1 = height;
            intermediate = length;
        }
        smaller2 = intermediate > width ? width : intermediate;
        totalRibbon += 2 * (smaller1 + smaller2) + height * length * width;
    }
    return totalRibbon;
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

    string content((istreambuf_iterator<char>(file)), (istreambuf_iterator<char>()));
    file.close();
    Input dimensions;
    regex instructions_regex("(\\d+)x(\\d+)x(\\d+)");
    for (sregex_iterator i = sregex_iterator(content.begin(), content.end(), instructions_regex);
         i != sregex_iterator(); i++)
    {
        smatch match = *i;
        dimensions.push_back(Dimension { stoi(match.str(1)), stoi(match.str(2)), stoi(match.str(3)) });
    }
    return dimensions;
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

#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <sstream>
#include <algorithm>
#include <cmath>

using namespace std;

struct Results
{
    int part1;
    int part2;
};

struct Connection
{
    char wires[10];
    char displays[4];
};
typedef vector<Connection> Input;

int getBitCount(char wire)
{
    auto total = 0;
    while (wire)
    {
        total += wire & 1;
        wire >>= 1;
    }
    return total;
}

int part1(Input connections)
{
    auto total = 0;
    for (auto connection: connections)
    {
        total += count_if(connection.displays, connection.displays + 4, [](char display) { 
            switch (getBitCount(display))
            {
                case 2:
                case 3:
                case 4:
                case 7:
                    return true;
                default:
                    return false;
            }
        });
    }
    return total;
}

void filterAndRemove(Connection *connection, char *digits, char digit, int digitLength, char exceptDigit, char exceptLength)
{
    for (auto wire = 0; wire < 10; wire++)
    {
        auto segments = connection->wires[wire];
        if (!segments)
            continue;
        auto length = getBitCount(segments);
        if (length == digitLength && (!exceptLength || (getBitCount(segments & ~digits[exceptDigit]) == exceptLength)))
        {
            digits[digit] = segments;
            connection->wires[wire] = 0;
            return;
        }
    }
}

int getConnectionValue(Connection connection)
{
    char digits[10] = { 0 };
    filterAndRemove(&connection, digits, 7, 3, 0, 0);
    filterAndRemove(&connection, digits, 4, 4, 0, 0);
    filterAndRemove(&connection, digits, 1, 2, 0, 0);
    filterAndRemove(&connection, digits, 8, 7, 0, 0);
    filterAndRemove(&connection, digits, 3, 5, 1, 3);
    filterAndRemove(&connection, digits, 6, 6, 1, 5);
    filterAndRemove(&connection, digits, 2, 5, 4, 3);
    filterAndRemove(&connection, digits, 5, 5, 4, 2);
    filterAndRemove(&connection, digits, 0, 6, 4, 3);
    for (auto wire = 0; ; wire++)
        if (connection.wires[wire])
        {
            digits[9] = connection.wires[wire];
            break;
        }
    int total = 0;
    for (auto display = 0; display < 4; display++)
        for (auto digit = 0; digit < 10; digit++)
            if (connection.displays[display] == digits[digit])
                total += digit * ((int)pow(10, 3 - display));
    return total;
}

int part2(Input connections)
{
    auto total = 0;
    for (auto connection: connections)
        total += getConnectionValue(connection);
    return total;
}

Results solve(Input connections)
{
    return {part1(connections), part2(connections)};
}

char parseWire(string wire)
{
    auto segments = 0;
    for (auto c: wire)
        segments |= 1 << (c - 'a');
    return segments;
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    Input input;
    string line;
    while (getline(file, line))
    {
        Connection connection;
        stringstream ss(line);
        string segments;
        for (auto wire = 0; wire < 10; wire++)
        {
            ss >> segments;
            connection.wires[wire] = parseWire(segments);
        }
        ss >> segments;
        for (auto display = 0; display < 4; display++)
        {
            ss >> segments;
            connection.displays[display] = parseWire(segments);
        }
        input.push_back(connection);
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

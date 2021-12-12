#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <sstream>
#include <queue>
#include <algorithm>

using namespace std;

struct Results
{
    int part1;
    int part2;
};

struct Edge {
    string nodeA, nodeB;
};
typedef vector<Edge> Input;

struct QueueNode {
    string node;
    string path;
    bool smallRepeat;
};

vector<Edge> getNextEdges(const Input edges, const string node)
{
    vector<Edge> result;
    copy_if(edges.begin(), edges.end(), back_inserter(result), [node](Edge edge) { return edge.nodeA == node || edge.nodeB == node; });
    return result;
}

bool isLowercase(string node)
{
    for (auto c: node)
        if (c < 'a')
            return false;
    return true;
}

int findPaths(Input edges, bool repeat)
{
    int completePathCount = 0;
    queue<QueueNode> toCheck;
    toCheck.push((QueueNode) { "start", "start", !repeat });
    while (toCheck.size())
    {
        auto queueNode = toCheck.front();
        toCheck.pop();
        if (queueNode.node == "end")
            completePathCount++;
        else
            for (auto edge: getNextEdges(edges, queueNode.node))
            {
                string other = edge.nodeA == queueNode.node ? edge.nodeB : edge.nodeA;
                if (!(other == "start" || (queueNode.smallRepeat && isLowercase(other) && queueNode.path.find(other) != string::npos)))
                    toCheck.push((QueueNode) { 
                        other, 
                        queueNode.path + "," + other, 
                        queueNode.smallRepeat || (isLowercase(other) && queueNode.path.find(other) != string::npos)}
                    );
            }
    }
    return completePathCount;
}

Results solve(Input edges)
{
    return {findPaths(edges, false), findPaths(edges, true)};
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    string line, nodeA, nodeB;
    Input input;
    while (getline(file, line))
    {
        stringstream ss(line);
        getline(ss, nodeA, '-');
        getline(ss, nodeB, '-');
        input.push_back((Edge) { nodeA, nodeB });
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

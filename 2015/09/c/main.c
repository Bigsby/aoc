#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <limits.h>

typedef struct {
    int nodeA, nodeB, distance;
} Edge;
typedef struct {
    int count, capacity;
    int nodeCount;
    Edge *edges;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct {
    int size;
    int lastNode;
    int *nodes;
} Path;

Path addToPath(Path path, int newNode)
{
    Path newPath;
    newPath.size = path.size + 1;
    newPath.lastNode = newNode;
    newPath.nodes = malloc(newPath.size * sizeof(int));
    if (path.size)
        memcpy(newPath.nodes, path.nodes, path.size * sizeof(int));
    newPath.nodes[newPath.size - 1] = newNode;
    return newPath;
}

int pathContains(Path path, int node)
{
    for (int index = 0; index < path.size; index++)
        if (path.nodes[index] == node)
            return 1;
    return 0;
}

typedef struct {
    Path path;
    int distance;
} StackItem;

#define STACK_INCREMENT 5
typedef struct {
    int head, capacity;
    StackItem *items;
} Stack;

void pushToStack(Stack *stack, Path previousPath, int newNode, int distance)
{
    if (stack->head == stack->capacity - 1)
    {
        stack->capacity += STACK_INCREMENT;
        StackItem *oldItems = stack->items;
        StackItem *newItems = realloc(oldItems, stack->capacity * sizeof(StackItem));
        stack->items = newItems;
    }
    stack->items[++stack->head] = (StackItem){
        addToPath(previousPath, newNode),
        distance
    };
}

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))

int getBestPathDistance(Input input, int longest)
{
    Stack stack = { 
        -1, STACK_INCREMENT,
        malloc(STACK_INCREMENT * sizeof(StackItem))
    };
    for (int node = 0; node < input.nodeCount; node++)
        pushToStack(&stack, (Path){0, 0, NULL}, node, 0);
    Path path;
    int distance, bestDistance = longest ? 0 : INT_MAX, newDistance;
    int currentNode, edgeIndex, nextNode;
    Edge edge;
    StackItem item;
    while (stack.head != -1)
    {
        item = stack.items[stack.head--];
        path = item.path;
        distance = item.distance;
        currentNode = path.lastNode;
        for (edgeIndex = 0; edgeIndex < input.count; edgeIndex++)
        {
            edge = input.edges[edgeIndex];
            if (edge.nodeA == currentNode || edge.nodeB == currentNode)
            {
                nextNode = edge.nodeA == currentNode ? edge.nodeB : edge.nodeA;
                if (pathContains(path, nextNode))
                    continue;
                newDistance = distance + edge.distance;
                if (!longest && newDistance > bestDistance)
                    continue;
                if (path.size == input.nodeCount - 1)
                    bestDistance = longest ? MAX(bestDistance, newDistance) : MIN(bestDistance, newDistance);
                else 
                    pushToStack(&stack, path, nextNode, newDistance);
            }
        }
        free(path.nodes);
    }
    free(stack.items);
    return bestDistance;
}

Results solve(Input input)
{
    return (Results){ getBestPathDistance(input, 0), getBestPathDistance(input, 1) };
}

#define INPUT_INCREMENT 5
typedef struct {
    int count, capacity;
    char **names;
} Names;

int getNodeIndex(Names *names, const char *name)
{
    for (int index = 0; index < names->count; index++)
        if (!strcmp(names->names[index], name))
            return index;
    if (names->count == names->capacity)
    {
        names->capacity += INPUT_INCREMENT;
        char **oldNames = names->names;
        char **newNames = realloc(oldNames, names->capacity * sizeof(char*));
        names->names = newNames;
    }
    names->names[names->count] = malloc(strlen(name) + 1);
    strcpy(names->names[names->count], name);
    return names->count++;
}

void addToInput(Input *input, Names *names, const char *nodeA, const char *nodeB, int distance)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        Edge *oldEdges = input->edges;
        Edge *newEdges = realloc(oldEdges, input->capacity * sizeof(Edge));
        input->edges = newEdges;
    }
    input->edges[input->count] = (Edge){
        getNodeIndex(names, nodeA),
        getNodeIndex(names, nodeB),
        distance};
    input->count++;
    input->nodeCount = names->count;
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    Input input = {
        0, INPUT_INCREMENT,
        0,
        malloc(INPUT_INCREMENT * sizeof(Edge))};
    Names names = {
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(char*))};
    char *line = NULL, nodeA[16], nodeB[16];
    size_t lineLength;
    int distance;
    while (getline(&line, &lineLength, file) != EOF)
    {
        if (sscanf(line, "%[^ ] to %[^ ] = %d", &nodeA, &nodeB, &distance) == 3)
            addToInput(&input, &names, nodeA, nodeB, distance);
        else {
            perror("Bad format line.");
            perror(line);
            exit(1);
        }
    }
    free(names.names);
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.edges);
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        perror("Please, add input file path as parameter");
        exit(1);
    }
    struct timeval starts, ends;
    gettimeofday(&starts, NULL);
    Input input = getInput(argv[1]);
    Results results = solve(input);
    gettimeofday(&ends, NULL);
    freeInput(input);
    printf("P1: %d\n", results.part1);
    printf("P2: %d\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}

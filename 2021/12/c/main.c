#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct {
    char nodeA, nodeB;
} Edge;

typedef struct {
    Edge *edges;
    int size, capacity;
} Input;

typedef struct {
    char **names;
    int size;
} Edges;

typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct {
    char node, *path;
    int pathSize, smallRepeat;
} QueueNode;

typedef struct {
    QueueNode *nodes;
    int size, capacity;
} Queue;

typedef struct {
    char *nodes;
    int count;
} NextNodes;

int isInPath(char node, char *path, int pathSize)
{
    while(pathSize--)
        if (*path++ == node)
            return 1;
    return 0;
}

#define QUEUE_INCREMENT 20
void addToQueue(Queue *queue, char node, char *path, int pathSize, int smallRepeat)
{
    if (queue->size == queue->capacity)
        queue->nodes = realloc(queue->nodes, (queue->capacity += QUEUE_INCREMENT) * sizeof(QueueNode));
    QueueNode queueNode = {
        node,
        malloc(pathSize + 1),
        pathSize + 1,
        smallRepeat || (node < 0 && isInPath(node, path, pathSize))
    };
    memcpy(queueNode.path, path, pathSize);
    queueNode.path[pathSize] = node;
    queue->nodes[queue->size++] = queueNode;
}

QueueNode getFromQueue(Queue *queue)
{
    return queue->nodes[queue->size-- - 1];
}

NextNodes getNextNodes(Input input, char node)
{
    NextNodes next = {
        malloc(20 * sizeof(char)),
        0
    };
    while (input.size--)
    {
        Edge edge = *input.edges++;
        if (edge.nodeA == node)
            next.nodes[next.count++] = edge.nodeB;
        if (edge.nodeB == node)
            next.nodes[next.count++] = edge.nodeA;
    }
    return next;
}

#define START 0
#define END -1
int findPaths(Input input, int repeat)
{
    int completePathsCount = 0;
    Queue queue = {
        malloc(QUEUE_INCREMENT * sizeof(QueueNode)),
        0, QUEUE_INCREMENT
    };
    addToQueue(&queue, START, "\0", 1, !repeat);
    while (queue.size)
    {
        QueueNode queueNode = getFromQueue(&queue);
        if (queueNode.node == END)
        {
            completePathsCount++;
            continue;
        } else
        {
            NextNodes next = getNextNodes(input, queueNode.node);
            for (int index = 0; index < next.count; index++)
            {
                char other = next.nodes[index];
                if (!(other == START || (queueNode.smallRepeat && other < 0 && isInPath(other, queueNode.path, queueNode.pathSize))))
                    addToQueue(&queue, other, queueNode.path, queueNode.pathSize, queueNode.smallRepeat);
            }
            free(next.nodes);
        }
        free(queueNode.path);
    }
    free(queue.nodes);
    return completePathsCount;
}

Results solve(Input input)
{
    return (Results){findPaths(input, 0), findPaths(input, 1)};
}

int isLowerCase(char *name)
{
    while (*name)
        if (*name++ < 'a')
            return 0;
    return 1;
}

char getEdge(Edges *edges, char *name)
{
    int lowerMultiplier = isLowerCase(name) ? -1 : 1;
    for (int index = 0; index < edges->size; index++)
        if (!strcmp(edges->names[index], name))
            return index * lowerMultiplier;
    edges->names[edges->size] = malloc(3 * sizeof(char));
    strcpy(edges->names[edges->size], name);
    return (edges->size++) * lowerMultiplier;
}

#define INPUT_INCREMENT 5
void addToInput(Input *input, char *nodeA, char *nodeB, Edges *edges)
{
    if (input->size == input->capacity)
        input->edges = realloc(input->edges, (input->capacity += INPUT_INCREMENT) * sizeof(Edge));
    input->edges[input->size++] = (Edge) { getEdge(edges, nodeA), getEdge(edges, nodeB) };
}

char *rtrim(char *str, const char *seps)
{
    int i;
    if (seps == NULL)
        seps = "\t\n\v\f\r ";
    i = strlen(str) - 1;
    while (i >= 0 && strchr(seps, str[i]) != NULL)
        str[i--] = '\0';
    return str;
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
        malloc(INPUT_INCREMENT * sizeof(Edge)),
        0, INPUT_INCREMENT
    };
    Edges edges = {
        malloc(100 * sizeof(char *)),
        0
    };
    edges.names[0] = malloc(strlen("start") * sizeof(char));
    strcpy(edges.names[0], "start");
    edges.names[1] = malloc(strlen("end") * sizeof(char));
    strcpy(edges.names[1], "end");
    edges.size = 2;
    char *line = NULL, *nodeA, *nodeB;
    size_t len;
    while (getline(&line, &len, file) != EOF)
    {
        nodeA = strtok(line, "-");
        nodeB = strtok(NULL, "-");
        addToInput(&input, nodeA, rtrim(nodeB, NULL), &edges);
    }
    fclose(file);
    free(edges.names);
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

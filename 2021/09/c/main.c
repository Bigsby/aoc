#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct {
    int **map;
    int maxX, maxY, capacity;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct {
    int x, y;
} Position;

typedef struct {
    Position positions[4];
    int count;
} Neighbors;

typedef struct {
    Position *positions;
    int size, capacity;
} Visited;

typedef struct {
    Position *positions;
    int current, size, capacity;
} Queue;

Neighbors getNeighbors(Input input, Position position)
{
    Neighbors neighbors;
    neighbors.count = 0;
    if (position.x)
        neighbors.positions[neighbors.count++] = (Position){ position.x - 1, position.y };
    if (position.y)
        neighbors.positions[neighbors.count++] = (Position){ position.x, position.y - 1 };
    if (position.x < input.maxX - 1)
        neighbors.positions[neighbors.count++] = (Position){ position.x + 1, position.y };
    if (position.y < input.maxY - 1)
        neighbors.positions[neighbors.count++] = (Position){ position.x, position.y + 1 };
    return neighbors;
}

int getPositionRisk(Input input, Position position)
{
    int height = input.map[position.y][position.x];
    Neighbors neighbors = getNeighbors(input, position);
    for (int neighborIndex = 0; neighborIndex < neighbors.count; neighborIndex++)
    {
        Position neighbor = neighbors.positions[neighborIndex];
        if (input.map[neighbor.y][neighbor.x] <= height)
            return 0;
    }
    return height + 1;
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

#define LIST_INCREMENT 10
int isQueueEmpty(Queue queue)
{
    return queue.current == queue.size;
}

void addToQueue(Queue *queue, Position position)
{
    if (queue->size == queue->capacity)
    {
        queue->capacity += LIST_INCREMENT;
        queue->positions = realloc(queue->positions, queue->capacity * sizeof(Position));
    }
    queue->positions[queue->size++] = position;
}

Position dequeue(Queue *queue)
{
    return queue->positions[queue->current++];
}
    
int isInVisited(Visited visited, Position position)
{
    while (visited.size--)
    {
        Position visitedPosition = *visited.positions++;
        if (visitedPosition.x == position.x && visitedPosition.y == position.y)
            return 1;
    }
    return 0;
}

void addToVisited(Visited *visited, Position position)
{
    if (visited->size == visited->capacity)
    {
        visited->capacity += LIST_INCREMENT;
        visited->positions = realloc(visited->positions, visited->capacity * sizeof(Position));
    }
    visited->positions[visited->size++] = position;
}

int getBasinSize(Input input, Position position)
{
    Queue queue = {
        malloc(LIST_INCREMENT * sizeof(Position)),
        0, 0, LIST_INCREMENT
    };
    Visited visited = {
        malloc(LIST_INCREMENT * sizeof(Position)),
        0, LIST_INCREMENT
    };
    addToQueue(&queue, position);
    while (!isQueueEmpty(queue))
    {
        Position current = dequeue(&queue);
        if (isInVisited(visited, current))
            continue;
        addToVisited(&visited, current);
        int currentHeight = input.map[current.y][current.x];
        Neighbors neighbors = getNeighbors(input, current);
        for (int neighborIndex = 0; neighborIndex < neighbors.count; neighborIndex++)
        {
            Position neighbor = neighbors.positions[neighborIndex];
            int neighborHeight = input.map[neighbor.y][neighbor.x];
            if (neighborHeight == 9 || neighborHeight <= currentHeight || isInVisited(visited, neighbor))
                continue;
            addToQueue(&queue, neighbor);
        }
    }
    free(queue.positions);
    free(visited.positions);
    return visited.size;
}

Results solve(Input input)
{
    int lowestSum = 0;
    int sizes[3] = { 0 };
    for (int y = 0; y < input.maxY; y++)
        for (int x = 0; x < input.maxX; x++)
        {
            Position position =  { .x = x, .y = y };
            int positionRisk = getPositionRisk(input, position);
            if (positionRisk)
            {
                lowestSum += positionRisk;
                addToSizes(sizes, getBasinSize(input, position));
            }
        }
    return (Results){ lowestSum, sizes[0] * sizes[1] * sizes[2] };
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int *row)
{
    if (input->capacity == input->maxY)
    {
        input->capacity += INPUT_INCREMENT;
        input->map = realloc(input->map, input->capacity * sizeof(int *));
    }
    input->map[input->maxY++] = row;
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
        malloc(INPUT_INCREMENT * sizeof(int *)),
        0, 0, INPUT_INCREMENT
    };
    char *line = NULL, c;
    size_t len;
    while (getline(&line, &len, file) != EOF)
    {
        input.maxX = strlen(line) - 1;
        int *row = malloc(sizeof(int) * (input.maxX));
        for (int x = 0; x < input.maxX; x++)
            row[x] = line[x] - '0';
        addToInput(&input, row);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    for (int y = 0; y < input.maxY; y++)
        free(input.map[y]);
    free(input.map);
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

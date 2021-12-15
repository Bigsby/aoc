#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <limits.h>

typedef struct {
    char **riskLevels;
    int size, capacity;
    int width, height;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct {
    int x, y;
} Point;

typedef struct PriorityNode {
    Point point;
    int distance;
    struct PriorityNode *next;
} PriorityNode;

typedef struct {
    Point points[4];
    int count;
} Neighbors;

int pointEquals(Point a, Point b)
{
    return a.x == b.x && a.y == b.y;
}

int **createDistances(int width, int height)
{
    int **distances = malloc(height * sizeof(int*));
    for (int y = 0; y < height; y++)
    {
        distances[y] = malloc(width * sizeof(int));
        for (int x = 0; x < width; x++)
            distances[y][x] = INT_MAX;
    }
    return distances;
}

void freeDistances(int **distances, int height)
{
    for (int y = 0; y < height; y++)
        free(distances[y]);
    free(distances);
}

Neighbors getNeighbors(Point point, int width, int height)
{
    Neighbors neighbors;
    neighbors.count = 0;
    if (point.x)
        neighbors.points[neighbors.count++] = (Point){ point.x - 1, point.y };
    if (point.y)
        neighbors.points[neighbors.count++] = (Point){ point.x, point.y - 1 };
    if (point.x < width - 1)
        neighbors.points[neighbors.count++] = (Point){ point.x + 1, point.y };
    if (point.y < height - 1)
        neighbors.points[neighbors.count++] = (Point){ point.x, point.y + 1};
    return neighbors;
}

PriorityNode *addToPriorityQueue(PriorityNode *node, Point point, int distance)
{
    PriorityNode *current = node;
    PriorityNode *last = NULL;
    while (current != NULL && current->distance < distance)
    {
        last = current;
        current = current->next;
    }
    PriorityNode *new = malloc(sizeof(PriorityNode));
    new->point = point;
    new->distance = distance;
    new->next = current;
    if (last != NULL)
        last->next = new;
    return last == NULL ? new : node;
}

PriorityNode *getNextPoint(PriorityNode *node, Point *point, int *distance)
{
    if (node == NULL)
    {
        perror("Empty queue");
        exit(1);
    }
    *point = node->point;
    *distance = node->distance;
    PriorityNode *next = node->next;
    free(node);
    return next;
}

char getPointRisk(Input input, Point point, int expansion)
{
    int risk = input.riskLevels[point.y % input.height][point.x % input.width] + point.x / input.width + point.y / input.height;
    return risk < 10 ? risk : risk - 9;
}

int getLowestRisk(Input input, int expansion)
{
    int expandedWidth = input.width * expansion;
    int expandedHeight = input.height * expansion;
    int **distances = createDistances(expandedWidth, expandedHeight);
    Point target = (Point){ expandedWidth - 1, expandedHeight - 1 };
    distances[0][0] = 0;
    PriorityNode *queue = NULL;
    queue = addToPriorityQueue(queue, (Point){ 0, 0 }, 0);
    Point current;
    int currentDistance;
    while (1)
    {
        queue = getNextPoint(queue, &current, &currentDistance);
        if (pointEquals(current, target))
        {
            freeDistances(distances, expandedHeight);
            free(queue);
            return currentDistance;
        }
        Neighbors neighbors = getNeighbors(current, expandedWidth, expandedHeight);
        while (neighbors.count--)
        {
            Point neighbor = neighbors.points[neighbors.count];
            int neighborRisk = currentDistance + getPointRisk(input, neighbor, expansion);
            if (distances[neighbor.y][neighbor.x] > neighborRisk)
            {
                distances[neighbor.y][neighbor.x] = neighborRisk;
                queue = addToPriorityQueue(queue, neighbor, neighborRisk);
            }
        }
    }
}

Results solve(Input input)
{
    return (Results){getLowestRisk(input, 1), getLowestRisk(input, 5)};
}

#define INPUT_INCREMENT 10
void addRowToInput(Input *input, char *row)
{
    if (input->size == input->capacity)
        input->riskLevels = realloc(input->riskLevels, (input->capacity += INPUT_INCREMENT) * sizeof(char*));
    input->riskLevels[input->size++] = row;
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
        .riskLevels = malloc(INPUT_INCREMENT * sizeof(char *)),
        .size = 0,
        .capacity = INPUT_INCREMENT
    };
    char *line = NULL, *row, c;
    size_t len;
    int x, y = 0;
    while (getline(&line, &len, file) != EOF)
    {
        if (input.width == 0)
            input.width = strlen(line) - 1;
        addRowToInput(&input, malloc(input.width * sizeof(char)));
        for (x = 0; x < input.width; x++)
            input.riskLevels[y][x] = line[x] - '0';
        y++;
    }
    input.height = y;
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.riskLevels);
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

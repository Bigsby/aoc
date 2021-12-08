#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>
#include <complex.h>
#include <math.h>
#include <limits.h>

#define MAX_COUNT 1024
#define NOT_FOUND -1

typedef double complex Lattice;

typedef struct
{
    Lattice direction;
    int distance;
} Direction;

typedef struct
{
    Direction *directions;
    int count;
    int size;
} Wire;

typedef struct
{
    Wire wireA;
    Wire wireB;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct PathNode
{
    int x, y, steps;
    struct PathNode *left;
    struct PathNode *right;
} PathNode;

int min(int a, int b)
{
    return a < b ? a : b;
}

int comparePositions(int aX, int aY, int bX, int bY)
{
    if (aY > bY)
        return 1;
    if (aY < bY)
        return -1;
    if (aX > bX)
        return 1;
    if (aX < bX)
        return -1;
    return 0;
}

PathNode *addToPath(PathNode *node, int x, int y, int steps)
{
    int compare;
    if (node == NULL)
    {
        node = malloc(sizeof(PathNode));
        node->x = x;
        node->y = y;
        node->steps = steps;
        node->left = node->right = NULL;
    }
    else if ((compare = comparePositions(node->x, node->y, x, y)) == 1)
        node->left = addToPath(node->left, x, y, steps);
    else if (compare == -1)
        node->right = addToPath(node->right, x, y, steps);
    return node;
}

PathNode *addLatticeToPath(PathNode *node, Lattice position, int steps)
{
    return addToPath(node, creal(position), cimag(position), steps);
}

int pathContains(PathNode *node, int x, int y)
{
    if (node == NULL)
        return 0;
    int compare = comparePositions(node->x, node->y, x, y);
    if (compare == 0)
        return 1;
    return compare == 1 ? pathContains(node->left, x, y) : pathContains(node->right, x, y);
}

int pathContainsLattice(PathNode *node, Lattice position)
{
    return pathContains(node, creal(position), cimag(position));
}

int getSteps(PathNode *node, int x, int y)
{
    if (node == NULL)
        return NOT_FOUND;
    int compare = comparePositions(node->x, node->y, x, y);
    if (compare == 0)
        return node->steps;
    return compare == 1 ? getSteps(node->left, x, y) : getSteps(node->right, x, y);
}

int getStepsForLattice(PathNode *node, Lattice position)
{
    return getSteps(node, creal(position), cimag(position));
}

void freePath(PathNode *node)
{
    free(node->left);
    free(node->right);
    if (node != NULL)
        free(node);
}

PathNode *getWirePositionSet(Wire wire)
{
    PathNode *positionSet = NULL;
    Lattice position = 0, direction;
    int distance;
    int steps;
    while (wire.count--)
    {
        direction = wire.directions->direction;
        for (distance = 0; distance < wire.directions->distance; distance++)
        {
            position += direction;
            steps++;
            positionSet = addLatticeToPath(positionSet, position, steps);
        }
        wire.directions++;
    }
    return positionSet;
}

int getManhatanDistance(Lattice position)
{
    return fabs(creal(position)) + fabs(cimag(position));
}

Results solve(Input input)
{
    PathNode *wireAPoints = getWirePositionSet(input.wireA);
    Wire wireB = input.wireB;
    int shortestManhatan = INT_MAX, shortestSteps = INT_MAX, steps = 0, distance;
    Lattice position = 0, direction;
    while (wireB.count--)
    {
        direction = wireB.directions->direction;
        for (distance = 0; distance < wireB.directions->distance; distance++)
        {
            position += direction;
            steps++;
            if (pathContainsLattice(wireAPoints, position))
            {
                shortestManhatan = min(shortestManhatan, getManhatanDistance(position));
                shortestSteps = min(shortestSteps, steps + getStepsForLattice(wireAPoints, position));
            }
        }
        wireB.directions++;
    }
    
    return (Results){shortestManhatan, shortestSteps};
}

#define WIRE_INCREMENT 10
Wire createWire()
{
    return (Wire){
        calloc(WIRE_INCREMENT, sizeof(Direction)),
        0,
        WIRE_INCREMENT};
}

void addToWire(Wire *wire, Lattice direction, int distance)
{
    if (wire->count == wire->size)
    {
        wire->size += WIRE_INCREMENT;
        wire->directions = realloc(wire->directions, wire->size * sizeof(Direction));
    }
    wire->directions[wire->count].direction = direction;
    wire->directions[wire->count].distance = distance;
    wire->count++;
}

Lattice getDirectionFromChar(char c)
{
    switch (c)
    {
    case 'R':
        return 1;
    case 'U':
        return I;
    case 'L':
        return -1;
    case 'D':
        return -I;
    }
    perror("Unknown direction");
    exit(1);
}

regex_t regexCompiled;
regmatch_t groupArray[MAX_COUNT];
Wire parseWire(char *cursor)
{
    Lattice direction;
    int group, distance;
    Wire wire = createWire();
    while (!regexec(&regexCompiled, cursor, MAX_COUNT, groupArray, 0))
    {
        for (group = 0; group <= 2 && groupArray[group].rm_so != -1; group++)
        {
            char cursorCopy[strlen(cursor) + 1];
            strcpy(cursorCopy, cursor);
            cursorCopy[groupArray[group].rm_eo] = 0;
            switch (group)
            {
            case 1:
                direction = getDirectionFromChar(*(cursorCopy + groupArray[group].rm_so));
                break;
            case 2:
                distance = atoi(cursorCopy + groupArray[group].rm_so);
                break;
            }
        }
        cursor += groupArray[0].rm_eo;
        addToWire(&wire, direction, distance);
    }
    return wire;
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }

    if (regcomp(&regexCompiled, "(R|U|L|D)([0-9]+)", REG_EXTENDED))
    {
        perror("Error compiling regex.");
        exit(1);
    }
    size_t lineLength;
    char *line = NULL;
    getline(&line, &lineLength, file);
    Wire wireA = parseWire(line);
    getline(&line, &lineLength, file);
    Wire wireB = parseWire(line);
    fclose(file);
    return (Input){wireA, wireB};
}

void freeInput(Input input)
{
    free(input.wireA.directions);
    free(input.wireB.directions);
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

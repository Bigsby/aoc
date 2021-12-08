#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>
#include <math.h>
#include <limits.h>

typedef struct
{
    int x, y;
} Lattice;

typedef struct
{
    int count, capacity;
    Lattice *positions;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct
{
    int xStart, xEnd, yStart, yEnd;
} Edges;

int getManhatanDistance(Lattice positionA, Lattice positionB)
{
    return abs(positionA.x - positionB.x) + abs(positionA.y - positionB.y);
}

Edges getMapEdges(Input input)
{
    int xStart, xEnd, yStart, yEnd;
    xStart = yStart = INT_MAX;
    xEnd = yEnd = INT_MIN;
    Lattice currentPosition;
    while (input.count--)
    {
        currentPosition = *(input.positions++);
        xStart = currentPosition.x < xStart ? currentPosition.x : xStart;
        xEnd = currentPosition.x > xEnd ? currentPosition.x : xEnd;
        yStart = currentPosition.y < yStart ? currentPosition.y : yStart;
        yEnd = currentPosition.y > yEnd ? currentPosition.y : yEnd;
    }
    return (Edges){xStart, xEnd, yStart, yEnd};
}

#define NO_CLOSEST -1
int findClosesLocation(Lattice position, Input input)
{
    int closest = NO_CLOSEST, closestDistance = INT_MAX, index = 0, distance;
    while (index < input.count)
    {
        distance = getManhatanDistance(position, input.positions[index]);
        if (distance < closestDistance)
        {
            closest = index;
            closestDistance = distance;
        }
        else if (distance == closestDistance)
            closest = NO_CLOSEST;
        index++;
    }
    return closest;
}

int part1(Input input, Edges edges)
{
    int *locationCounts = calloc(input.count, sizeof(int));
    int x, y, closest;
    for (y = edges.yStart + 1; y < edges.yEnd; y++)
        for (x = edges.xStart + 1; x < edges.xEnd; x++)
            if ((closest = findClosesLocation((Lattice){x, y}, input)) != NO_CLOSEST)
                locationCounts[closest]++;
    for (y = edges.yStart; y < edges.yEnd + 1; y++)
    {
        if ((closest = findClosesLocation((Lattice){edges.xStart, y}, input)) != NO_CLOSEST)
            locationCounts[closest] = 0;
        if ((closest = findClosesLocation((Lattice){edges.xEnd, y}, input)) != NO_CLOSEST)
            locationCounts[closest] = 0;
    }
    for (x = edges.xStart; x < edges.xEnd + 1; x++)
    {
        if ((closest = findClosesLocation((Lattice){x, edges.yStart}, input)) != NO_CLOSEST)
            locationCounts[closest] = 0;
        if ((closest = findClosesLocation((Lattice){x, edges.yEnd}, input)) != NO_CLOSEST)
            locationCounts[closest] = 0;
    }
    int max = 0, count, index = 0;
    while (input.count--)
        max = (count = locationCounts[index++]) > max ? count : max;
    return max;
}

int getDistancesSum(Lattice position, Input input)
{
    int total = 0;
    while (input.count--)
        total += getManhatanDistance(position, *(input.positions++));
    return total;
}

const int MAX_DISTANCE = 10000;
int part2(Input input, Edges edges)
{
    int validLocationsCount = 0, x, y;
    for (y = edges.yStart; y < edges.yEnd + 1; y++)
        for (x = edges.xStart; x < edges.xEnd + 1; x++)
            validLocationsCount += getDistancesSum((Lattice){x, y}, input) < MAX_DISTANCE;
    return validLocationsCount;
}

void printPositions(Input input)
{
    while (input.count--)
    {
        Lattice position = *(input.positions++);
        printf("%d, %d\n", position.x, position.y);
    }
}

Results solve(Input input)
{
    Edges edges = getMapEdges(input);
    return (Results){part1(input, edges), part2(input, edges)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int x, int y)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->positions = realloc(input->positions, input->capacity * sizeof(Lattice));
    }
    input->positions[input->count++] = (Lattice){x, y};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
#define INPUT_REGEX_GROUP_COUNT 4
    regex_t inputRegex;
    if (regcomp(&inputRegex, "^([0-9]+), ([0-9]+)", REG_EXTENDED))
    {
        perror("Error compiling hgt regex.");
        exit(1);
    }
    Input input = {
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(Lattice))};
    char *line = NULL, *cursor = NULL;
    size_t lineLength;
    regmatch_t groupArray[INPUT_REGEX_GROUP_COUNT];
    int group, x, y;
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        if (!regexec(&inputRegex, cursor, INPUT_REGEX_GROUP_COUNT, groupArray, 0))
        {
            for (group = 0; group <= INPUT_REGEX_GROUP_COUNT && groupArray[group].rm_so != -1; group++)
            {
                char cursorCopy[strlen(cursor) + 1];
                strcpy(cursorCopy, cursor);
                cursorCopy[groupArray[group].rm_eo] = 0;
                switch (group)
                {
                case 1:
                    x = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    y = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                }
            }
            cursor += groupArray[0].rm_eo;
            addToInput(&input, x, y);
        }
        else
        {
            perror("Bad format line");
            perror(line);
            exit(1);
        }
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.positions);
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

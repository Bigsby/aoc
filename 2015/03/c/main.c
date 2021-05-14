#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <complex.h>

typedef double complex Lattice;

typedef struct
{
    Lattice *direction;
    int count;
} Input;

typedef struct
{
    int part1;
    int part2;
} Results;

struct Visited
{
    Lattice position;
    struct Visited *next;
    int count;
};

void addVisited(struct Visited *head, Lattice position)
{
    struct Visited *initialHead = head;
    struct Visited *previous = NULL;
    while (head != NULL)
    {
        if (head->position == position)
            return;
        previous = head;
        head = head->next;
    }
    struct Visited *newVisited = malloc(sizeof(struct Visited));
    newVisited->position = position;
    newVisited->next = NULL;
    previous->next = newVisited;
    initialHead->count++;
}

Lattice processDirection(struct Visited *visitedHouses, Lattice position, Lattice direction)
{
    position += direction;
    addVisited(visitedHouses, position);
    return position;
}

int part1(Input input)
{
    Lattice position = 0;
    struct Visited *visitedHouses = malloc(sizeof(struct Visited));
    visitedHouses->position = position;
    visitedHouses->next = NULL;
    visitedHouses->count = 1;
    while (input.count--)
        position = processDirection(visitedHouses, position, *(input.direction++));
    return visitedHouses->count;
}

int part2(Input input)
{
    Lattice position = 0;
    struct Visited *visitedHouses = malloc(sizeof(struct Visited));
    visitedHouses->position = position;
    visitedHouses->next = NULL;
    visitedHouses->count = 1;
    Lattice santaPosition = 0, robotPosition = 0;
    int index = 0;
    while (input.count--)
    {
        if (index++ % 2 == 0)
            santaPosition = processDirection(visitedHouses, santaPosition, *input.direction);
        else 
            robotPosition = processDirection(visitedHouses, robotPosition, *input.direction);
        input.direction++;
    }
    return visitedHouses->count;
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    rewind(file);
    Lattice *directions = calloc(length, sizeof(Lattice));
    int count = 0;
    char c;
    while ((c = getc(file)) != EOF)
    {
        switch (c)
        {
        case '^':
            directions[count] = -I;
            break;
        case 'v':
            directions[count] = I;
            break;
        case '>':
            directions[count] = 1;
            break;
        case '<':
            directions[count] = -1;
            break;
        default:
            count--;
            break;
        }
        count++;
    }
    fclose(file);
    return (Input){
        directions,
        count};
}

void freeInput(Input input)
{
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
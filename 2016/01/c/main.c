#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <ctype.h>
#include <unistd.h>
#include <complex.h>
#include <math.h>

typedef struct Instruction
{
    char direction;
    int distance;
    struct Instruction *next;
} Instruction;

typedef Instruction *Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef double complex Lattice;

int getManhatanDistance(Lattice position)
{
    return (int)(fabs(creal(position)) + fabs(cimag(position)));
}

struct Visited
{
    Lattice position;
    struct Visited *next;
};

int isVisited(struct Visited *head, Lattice position)
{
    struct Visited *previous = NULL;
    while (head != NULL)
    {
        if (creal(head->position) == creal(position) && cimag(head->position) == cimag(position))
            return 1;
        previous = head;
        head = head->next;
    }
    struct Visited *newVisited = malloc(sizeof(struct Visited));
    newVisited->position = position;
    newVisited->next = NULL;
    previous->next = newVisited;
    return 0;
}

Results solve(Input input)
{
    int part2 = 0;
    Lattice heading = I;
    Lattice position = 0;
    struct Visited *visited = malloc(sizeof(struct Visited));
    visited->position = position;
    visited->next = NULL;
    Instruction *current = input;
    int step;
    while (current != NULL)
    {
        heading *= current->direction == 'L' ? I : -I;
        for (step = 0; step < current->distance; step++)
        {
            position += heading;
            if (part2 == 0)
                if (isVisited(visited, position))
                    part2 = getManhatanDistance(position);
        }
        current = current->next;
    }
    struct Visited *previous;
    while (visited != NULL)
    {
        previous = visited;
        visited = visited->next;
        free(previous);
    }
    return (Results){getManhatanDistance(position), part2};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    Instruction *start = NULL;
    Instruction *previous = NULL;
    int c = !EOF;
    char direction = 0;
    int distance = 0;
    int skip = 0;
    while (c != EOF)
    {
        c = getc(file);
        if (isalpha(c))
        {
            skip = 0;
            direction = c;
        }
        else if (isdigit(c))
            distance = distance * 10 + (c - '0');
        else if (!skip)
        {
            skip = 1;
            Instruction *newInstruction = malloc(sizeof(Instruction));
            newInstruction->direction = direction;
            newInstruction->distance = distance;
            newInstruction->next = NULL;
            distance = 0;
            if (previous)
                previous->next = newInstruction;
            else
                start = newInstruction;
            previous = newInstruction;
        }
    }
    fclose(file);
    return start;
}

void freeInput(Input input)
{
    Instruction *current = input;
    Instruction *previous;
    while (current != NULL)
    {
        previous = current;
        current = current->next;
        free(previous);
    }
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
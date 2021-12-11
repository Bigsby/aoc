#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct {
    char **octopuses;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;


typedef struct {
    int x, y;
} Lattice;

typedef struct {
    Lattice octopuses[100];
    int size;
} ToProcess;

typedef struct {
    Lattice octopuses[8];
    int count;
} Neighbors;

void addToNeighbors(Neighbors *neighbors, int x, int y)
{
    neighbors->octopuses[neighbors->count++] = (Lattice) { x, y };
}

Lattice getFromNeighbors(Neighbors *neighbors)
{
    return neighbors->octopuses[neighbors->count-- - 1];
}

void populateNeighbors(Neighbors *neighbors, int x, int y)
{
    neighbors->count = 0;
    if (x)
    {
        addToNeighbors(neighbors, x - 1, y);
        if (y)
            addToNeighbors(neighbors, x - 1, y - 1);
        if (y < 9)
            addToNeighbors(neighbors, x - 1, y + 1);
    }
    if (x < 9)
    {
        addToNeighbors(neighbors, x + 1, y);
        if (y)
            addToNeighbors(neighbors, x + 1, y - 1);
        if (y < 9)
            addToNeighbors(neighbors, x + 1, y + 1);
    }
    if (y)
        addToNeighbors(neighbors, x, y - 1);
    if (y < 9)
        addToNeighbors(neighbors, x, y + 1);
}

void addToProcess(ToProcess *process, int x, int y)
{
    process->octopuses[process->size++] = (Lattice) { x, y };
}

Lattice getFromProcess(ToProcess *process)
{
    return process->octopuses[process->size-- - 1];
}

Results solve(Input input)
{
    int flashes = 0;
    int allFlashes = 0;
    int step = 0;
    while (allFlashes == 0 || step <= 100)
    {
        step++;
        int stepFlashes = 0;
        ToProcess toProcess;
        toProcess.size = 0;
        for (int y = 0; y < 10; y++)
            for (int x = 0; x < 10; x++)
            {
                input.octopuses[y][x]++;
                if (input.octopuses[y][x] == 10)
                    addToProcess(&toProcess, x, y);
            }
        while (toProcess.size)
        {
            Lattice octopus = getFromProcess(&toProcess);
            if (input.octopuses[octopus.y][octopus.x] == 0)
                continue;
            stepFlashes += 1;
            input.octopuses[octopus.y][octopus.x] = 0;
            Neighbors neighbors;
            populateNeighbors(&neighbors, octopus.x, octopus.y);
            while (neighbors.count)
            {
                Lattice neighbor = getFromNeighbors(&neighbors);
                if (input.octopuses[neighbor.y][neighbor.x] == 0)
                    continue;
                input.octopuses[neighbor.y][neighbor.x]++;
                if (input.octopuses[neighbor.y][neighbor.x] == 10)
                    addToProcess(&toProcess, neighbor.x, neighbor.y);
            }
        }
        if (step <= 100)
            flashes += stepFlashes;
        if (stepFlashes == 100)
            allFlashes = step;
    }
    return (Results){flashes, allFlashes};
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
        malloc(10 * sizeof(char *))
    };
    char *line = NULL;
    size_t len;
    int y = 0;
    while (getline(&line, &len, file) != EOF)
    {
        input.octopuses[y] = malloc(10 * sizeof(char));
        for (int x = 0; x < 10; x++)
            input.octopuses[y][x] = line[x] - '0';
        y++;
    }
    fclose(file);
    return input;
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

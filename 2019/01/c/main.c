#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct
{
    int *masses;
    int count;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int part1(int mass)
{
    return mass / 3 - 2;
}

int part2(int mass)
{
    int total = 0;
    int currentMass = mass;
    while (1)
    {
        int fuel = currentMass / 3 - 2;
        if (fuel <= 0)
            return total;
        total += fuel;
        currentMass = fuel;
    }
}

int getTotal(Input input, int (*fuelCalculator)(int))
{
    int total = 0;
    while (input.count--)
        total += (*fuelCalculator)(*input.masses++);
    return total;
}

Results solve(Input input)
{
    return (Results){getTotal(input, &part1), getTotal(input, &part2)};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    char *line = NULL;
    size_t len = 0;
    size_t size = 16;
    int count = 0;
    int *masses = malloc(128 * sizeof(int));
    int *current = masses;
    while (getline(&line, &len, file) != EOF)
    {
        count++;
        *current = atoi(line);
        current++;
    }
    if (line)
        free(line);
    fclose(file);
    return (Input){masses, count};
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
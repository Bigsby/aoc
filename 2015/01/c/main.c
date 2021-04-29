#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>
#include <string.h>

typedef struct
{
    int *directions;
    int count;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int part1(Input input)
{
    int total = 0;
    while (input.count--)
        total += *input.directions++;
    return total;
}

int part2(Input input)
{
    int index;
    int currentFloor = 0;
    int totalCount = input.count;
    while (input.count--)
        if ((currentFloor += *input.directions++) == -1)
            return totalCount - input.count;
    return -1;
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
    int *directions = calloc(length, sizeof(int));
    int *start = directions;
    int c;
    rewind(file);
    while ((c = getc(file)) != EOF)
    {
        switch (c)
        {
        case '(':
            *directions = 1;
            break;
        case ')':
            *directions = -1;
            break;
        }
        directions++;
    }
    fclose(file);
    return (Input){start, length};
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
    Results results = solve(getInput(argv[1]));
    gettimeofday(&ends, NULL);
    printf("P1: %d\n", results.part1);
    printf("P2: %d\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}
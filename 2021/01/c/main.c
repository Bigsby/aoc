#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <limits.h>

typedef struct {
    int *depths;
    int count, capacity;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int part1(Input input)
{
    int increments = 0;
    int lastDepth = INT_MAX;
    while (input.count--)
    {
        if (*(input.depths) > lastDepth)
            increments++;
        lastDepth = *(input.depths++);
    }
    return increments;
}

int part2(Input input)
{
    int increments = 0;
    int lastDepth = INT_MAX;
    while (input.count-- > 2)
    {
        int depth = input.depths[0] + input.depths[1] + input.depths[2];
        if (depth > lastDepth)
            increments++;
        lastDepth = depth;
        input.depths++;
    }
    return increments;
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int depth)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->depths = realloc(input->depths, input->capacity * sizeof(int));
    }
    input->depths[input->count++] = depth;
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
        malloc(INPUT_INCREMENT * sizeof(int)),
        0, INPUT_INCREMENT
    };
    size_t len = 0;
    char *line;
    while (getline(&line, &len, file) != EOF)
        addToInput(&input, atoi(line));
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

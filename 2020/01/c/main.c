#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct
{
    int *numbers;
    int count;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int sum(int *numbers, int length)
{
    int total = 0;
    while (length--)
        total += *numbers++;
    return total;
}

int multiply(int *numbers, int length)
{
    int total = 1;
    while (length--)
        total *= *numbers++;
    return total;
}

int getCombination(Input numbers, int length)
{
    int i;
    int combination[length];
    int indexes[length];
    for (i = 0; i < length; i++)
        indexes[i] = length - i;
    while (1)
    {
        for (i = length; i--;)
            combination[i] = numbers.numbers[indexes[i] - 1];
        if (sum(combination, length) == 2020)
            return multiply(combination, length);
        i = 0;
        if (indexes[i]++ < numbers.count)
            continue;
        for (; indexes[i] >= numbers.count - i;)
            if (++i >= length)
                return 0;
        for (indexes[i]++; i; i--)
            indexes[i - 1] = indexes[i] + 1;
    }
}

Results solve(Input input)
{
    return (Results){getCombination(input, 2), getCombination(input, 3)};
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
    char *line = NULL;
    size_t len = 0;
    size_t read;
    size_t size = 16;
    int count = 0;
    int *numbers = malloc(256 * sizeof(int));
    int *current = numbers;
    while ((read = getline(&line, &len, file)) != EOF)
    {
        count++;
        *current = atoi(line);
        current++;
    }
    if (line)
        free(line);
    fclose(file);
    return (Input){numbers, count};
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
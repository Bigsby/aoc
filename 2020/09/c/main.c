#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <limits.h>

typedef struct {
    long *numbers;
    int size, capacity;
} Input;
typedef struct
{
    long part1;
    long part2;
} Results;

int hasNoValidPair(int index, Input input)
{
    long number = input.numbers[index];
    for (int testIndex = index - 25; testIndex < index; testIndex++)
    {
        long testNumber = input.numbers[testIndex];
        for (int pairIndex = index - 25; pairIndex < index; pairIndex++)
            if (pairIndex != testIndex && testNumber + input.numbers[pairIndex] == number)
                return 0;
    }
    return 1;
}

long getWeakness(Input input, long targetNumber)
{
    for (int startIndex = 0; startIndex < input.size; startIndex++)
    {
        long currentSum = 0;
        int length = 1;
        while (currentSum < targetNumber)
        {
            long min = LONG_MAX;
            long max = LONG_MIN;
            currentSum = 0;
            for (int index = startIndex; index < startIndex + length; index++)
            {
                long number = input.numbers[index];
                currentSum += number;
                min = number < min ? number : min;
                max = number > max ? number : max;
            }
            if (currentSum == targetNumber)
                return min + max;
            length += 1;
        }
    }
    perror("Weakness not found");
    exit(1);
}

Results solve(Input input)
{
    long part1Result = 0;
    for (int index = 25; index < input.size; index++)
        if (hasNoValidPair(index, input))
        {
            part1Result = input.numbers[index];
            break;
        }
    return (Results){part1Result, getWeakness(input, part1Result)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, long number)
{
    if (input->size == input->capacity)
        input->numbers = realloc(input->numbers, (input->capacity += INPUT_INCREMENT) * sizeof(long));
    input->numbers[input->size++] = number;
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
        malloc(INPUT_INCREMENT * sizeof(long)),
        0, INPUT_INCREMENT
    };
    char *line = NULL;
    size_t len;
    while (getline(&line, &len, file) != EOF)
        addToInput(&input, atol(line));
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.numbers);
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
    printf("P1: %ld\n", results.part1);
    printf("P2: %ld\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}

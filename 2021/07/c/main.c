#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct {
    int *crabs;
    int count, capacity;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

void swap(int *xp, int *yp)
{
    int temp = *xp;
    *xp = *yp;
    *yp = temp;
}

void bubbleSort(Input input)
{
    int i, j;
    for (i = 0; i < input.count; i++)
        for (j = 0; j < input.count - i - 1; j++)
            if (input.crabs[j] > input.crabs[j + 1])
                swap(&input.crabs[j], &input.crabs[j + 1]);
}

int part1(Input input)
{
    bubbleSort(input);
    int mean = input.crabs[input.count / 2];
    int total = 0;
    while (input.count--)
        total += abs(mean - *input.crabs++);
    return total;
}

int getDistanceCost(int posA, int posB)
{
    int distance = abs(posA - posB);
    return (distance * (distance + 1)) / 2;
}

int getAverage(Input input)
{
    int count = input.count;
    int total = 0;
    while (input.count--)
        total += *input.crabs++;
    return total / count;
}

int part2(Input input)
{
    int average = getAverage(input);
    int total = 0;
    while (input.count--)
        total += getDistanceCost(average, *input.crabs++);
    return total;
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int position)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->crabs = realloc(input->crabs, input->capacity * sizeof(int));
    }
    input->crabs[input->count++] = position;
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
    char *content = malloc(length);
    fread(content, 1, length, file);
    fclose(file);
    Input input = {
        malloc(INPUT_INCREMENT * sizeof(int)),
        0, INPUT_INCREMENT
    };
    char *position = strtok(content, ",");
    while (position != NULL)
    {
        addToInput(&input, atoi(position));
        position = strtok(NULL, ",");
    }
    free(content);
    return input;
}

void freeInput(Input input)
{
    free(input.crabs);
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

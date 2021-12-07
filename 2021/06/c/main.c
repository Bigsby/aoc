#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct {
    int *fishes;
    int count, capacity;
} Input;
typedef struct
{
    unsigned long part1;
    unsigned long part2;
} Results;

unsigned long runGenerations(Input input, int generations)
{
    unsigned long fishCounts[9] = {0};
    while (input.count--)
        fishCounts[*input.fishes++]++;
    while (generations--)
    {
        unsigned long fishesAtZero = fishCounts[0];
        for (int day = 0; day < 8; day++)
            fishCounts[day] = fishCounts[day + 1];
        fishCounts[8] = fishesAtZero;
        fishCounts[6] += fishesAtZero;
    }
    unsigned long fishes = 0;
    for (int day = 0; day < 9; day++)
        fishes += fishCounts[day];
    return fishes;
}

Results solve(Input input)
{
    return (Results){runGenerations(input, 80), runGenerations(input, 256)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int day)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->fishes = realloc(input->fishes, input->capacity * sizeof(int));
    }
    input->fishes[input->count++] = day;
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
    char *fish = strtok(content, ",");
    while (fish != NULL)
    {
        addToInput(&input, atoi(fish));
        fish = strtok(NULL, ",");
    }
    free(content);
    return input;
}

void freeInput(Input input)
{
    free(input.fishes);
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
    printf("P1: %lu\n", results.part1);
    printf("P2: %lu\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}

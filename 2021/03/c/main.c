#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct {
    int *numbers, bitLength;
    int count, capacity;
} Input;

typedef struct
{
    int part1;
    int part2;
} Results;

int getNthBit1Count(Input input, int index)
{
    int mask = 1 << index;
    int count = 0;
    while (input.count--)
        count += (*(input.numbers++) & mask) == mask;
    return count;
}

int part1(Input input)
{
    int gamma = 0, epsilon = 0, half = input.count / 2;
    for (int index = input.bitLength - 1; index >= 0; index--)
        if (getNthBit1Count(input, index) > half)
        {
            gamma = (gamma << 1) + 1;
            epsilon <<= 1;
        }
        else 
        {
            gamma <<= 1;
            epsilon = (epsilon <<  1) + 1;
        }
    return gamma * epsilon;
}

Input copyInput(Input input)
{
    size_t numbersSize = sizeof(int) * input.count;
    Input newInput = {
        malloc(numbersSize),
        input.bitLength,
        input.count,
        input.capacity
    };
    memcpy(newInput.numbers, input.numbers, numbersSize);
    return newInput;
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int number)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        int *oldNumbers = input->numbers;
        int *newNumbers = realloc(oldNumbers, input->capacity * sizeof(int));
        input->numbers = newNumbers;
    }
    input->numbers[input->count++] = number;
}

void filterNumbers(Input *input, int mask, int match)
{
    int *oldNumbers = input->numbers;
    int *oldStart = input->numbers;
    int oldCount = input->count;
    input->count = 0;
    input->capacity = INPUT_INCREMENT;
    input->numbers = malloc(INPUT_INCREMENT * sizeof(int));
    while (oldCount--)
    {
        if ((*oldNumbers & mask) == match)
            addToInput(input, *oldNumbers);
        oldNumbers++;
    }
    free(oldStart);
}

void processBit(Input *input, int index, int mostCommon)
{
    if (input->count == 1)
        return;
    int onesCount = getNthBit1Count(*input, index);
    int zerosCount = input->count - onesCount;
    int mask = 1 << index;
    filterNumbers(input, mask, mostCommon ^ onesCount < zerosCount ? mask : 0);
}

int part2(Input input)
{
    Input oxygen = copyInput(input);
    Input co2 = input;
    int index = input.bitLength - 1;
    while (oxygen.count > 1 || co2.count > 1)
    {
        processBit(&oxygen, index, 1);
        processBit(&co2, index, 0);
        index--;
    }
    int result = *oxygen.numbers * (*co2.numbers);
    free(oxygen.numbers);
    free(co2.numbers);
    return result;
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
    Input input = {
        malloc(sizeof(int) * INPUT_INCREMENT), 0,
        0, INPUT_INCREMENT
    };
    size_t len = 0;
    char *line;
    while (getline(&line, &len, file) != EOF)
    {
        addToInput(&input, strtol(line, NULL, 2));
        if (!input.bitLength)
            input.bitLength = strlen(line) - 1;
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

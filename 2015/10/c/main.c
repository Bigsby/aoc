#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <math.h>

typedef char *Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct {
    char c;
    int length;
} Sequence;

typedef struct {
    Sequence *sequences;
    int size, capacity;
} Result;
#define SEQUENCE_INCREMENT 100

void addToResult(Result *result, int length, char c)
{
    if (result->size == result->capacity)
        result->sequences = realloc(result->sequences, (result->capacity += SEQUENCE_INCREMENT) * sizeof(Sequence));
    result->sequences[result->size++] = (Sequence){ c, length };
}

char *processResult(Result result)
{
    char *sequence = calloc((result.size * 2), sizeof(char));
    char *start = sequence;
    for (int index = 0; index < result.size; index++)
    {
        Sequence current = result.sequences[index];
        *sequence = current.length + '0';
        sequence++;
        *sequence = current.c;
        sequence++;
    }
    free(result.sequences);
    return start;
}

char *getNextValue(char *value)
{
    Result result = {
        malloc(SEQUENCE_INCREMENT * sizeof(Sequence)),
        0, SEQUENCE_INCREMENT
    };
    unsigned int valueLength = strlen(value);
    int length = 1;
    char lastDigit = value[0];
    for (unsigned int index = 1; index < valueLength; index++)
    {
        if (value[index] == lastDigit)
            length++;
        else
        {
            addToResult(&result, length, lastDigit);
            lastDigit = value[index];
            length = 1;
        }
    }
    addToResult(&result, length, lastDigit);
    free(value);
    return processResult(result);
}

Results solve(Input input)
{
    char *currentValue = input;
    int part1 = 0;
    for (int turn = 0; turn < 50; turn++)
    {
        if (turn == 40)
            part1 = strlen(currentValue);
        currentValue = getNextValue(currentValue);
    }
    return (Results){part1, strlen(currentValue)};
}

char *rtrim(char *str, const char *seps)
{
    int i;
    if (seps == NULL)
        seps = "\t\n\v\f\r ";
    i = strlen(str) - 1;
    while (i >= 0 && strchr(seps, str[i]) != NULL)
        str[i--] = '\0';
    return str;
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
    return rtrim(content, NULL);
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

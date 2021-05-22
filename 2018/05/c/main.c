#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <math.h>
#include <limits.h>

typedef char *Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int countNoRepeats(char *polymer, char ignore)
{
    int length = strlen(polymer);
    char *letters = malloc(strlen(polymer) + 1);
    strcpy(letters, polymer);
    int hasChanges = 1, index, lastLetterIndex;
    char letter, lastLetter, upperIgnore = ignore - 32;
    while (hasChanges)
    {
        hasChanges = 0;
        index = 0;
        lastLetter = 0;
        lastLetterIndex = 0;
        while (index < length)
        {
            letter = letters[index++];
            if (letter == 0) continue;
            if (letter == ignore || letter == upperIgnore)
            {
                hasChanges = 1;
                letters[index - 1] = 0;
                continue;
            }
            if (abs(letter - lastLetter) == 32)
            {
                hasChanges = 1;
                lastLetter = 0;
                letters[lastLetterIndex] = letters[index - 1] = 0;
                continue;
            }
            lastLetter = letter;
            lastLetterIndex = index - 1;
        }
    }
    free(letters);
    int count = 0;
    while (length--)
        count += *(letters++) != 0;
    return count - 1;
}

int part2(Input input)
{
    int min = INT_MAX, test;
    for (char c = 'a'; c <= 'z'; c++)
        min = (test = countNoRepeats(input, c)) < min ? test : min;
    return min;
}

Results solve(Input input)
{
    return (Results){countNoRepeats(input, 0), part2(input)};
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
    char *input = malloc(length + 1);
    fread(input, 1, length, file);
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input);
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
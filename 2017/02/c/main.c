#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

#define MAX_COUNT 32

typedef struct {
    int *numbers;
    size_t len;
} Line;

typedef struct {
    Line *lines;
    size_t len;
} Input;

typedef struct
{
    int part1;
    int part2;
} Results;

int min(Line line)
{
    int minimum = line.numbers[0];
    while (line.len--)
    {
        if (*line.numbers < minimum)
            minimum = *line.numbers;
        line.numbers++;
    }
    return minimum;
}

int max(Line line)
{
    int maximum = line.numbers[0];
    while (line.len--)
    {
        if (*line.numbers > maximum)
            maximum = *line.numbers;
        line.numbers++;
    }
    return maximum;
}

Results solve(Input input)
{
    int total1 = 0, total2 = 0, lineIndex = 0;
    while (input.len--)
    {
        total1 += max(input.lines[lineIndex]) - min(input.lines[lineIndex]);
        for (int aIndex = 0; aIndex < input.lines[lineIndex].len; aIndex++)
            for (int bIndex = 0; bIndex < input.lines[lineIndex].len; bIndex++)
            {
                int a = input.lines[lineIndex].numbers[aIndex];
                int b = input.lines[lineIndex].numbers[bIndex];
                if (a > b && a % b == 0)
                    total2 += a / b;
            }
        lineIndex++;
    }
    return (Results){total1, total2};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    int lineCount = 0;
    Line lines[MAX_COUNT];
    size_t line_length;
    regex_t regexCompiled;
    regmatch_t groupArray[MAX_COUNT];
    int groups;
    if (regcomp(&regexCompiled, "[0-9]+", REG_EXTENDED)) {
        perror("Error compiling regex.");
        exit(1);
    }
    char *line = NULL;
    char *cursor = NULL;
    while (getline(&line, &line_length, file) != EOF)
    {
        cursor = line;
        lines[lineCount] = (Line) {
            calloc(32, sizeof(int)),
            0
        };
        int groups = 0;
        while (!regexec(&regexCompiled, cursor, MAX_COUNT, groupArray, 0))
        {
            char cursorCopy[strlen(cursor) + 1];
            strcpy(cursorCopy, cursor);
            cursorCopy[groupArray[0].rm_eo] = 0;
            lines[lineCount].numbers[groups++] = atoi(cursorCopy);
            lines[lineCount].len++;
            cursor += groupArray[0].rm_eo;
        }
        lineCount++;
    }
    fclose(file);
    return (Input){
        lines,
        lineCount
    };
}

void freeInput(Input input)
{
    int lineIndex = 0;
    while (input.len--)
        free(input.lines[lineIndex].numbers);
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
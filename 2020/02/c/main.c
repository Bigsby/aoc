#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

#define MAX_COUNT 1024

typedef struct
{
    int first;
    int second;
    char letter;
    char *password;
} Line;

typedef struct
{
    Line *lines;
    int count;
} Input;

typedef struct
{
    int part1;
    int part2;
} Results;

int countValid(Input input, int (*validationFunc)(Line *))
{
    int count = 0;
    while (input.count--)
        count += validationFunc(input.lines++);
    return count;
}

int isLineValid1(Line *line)
{
    char *password = line->password;
    int occurenceCount = 0;
    char c;
    while ((c = *password++))
        occurenceCount += c == line->letter;
    return occurenceCount >= line->first && occurenceCount <= line->second;
}

int isLineValid2(Line *line)
{
    return (line->password[line->first - 1] == line->letter) ^ (line->password[line->second - 1] == line->letter);
}

Results solve(Input input)
{
    return (Results){countValid(input, isLineValid1), countValid(input, isLineValid2)};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    regex_t regexCompiled;
    regmatch_t groupArray[MAX_COUNT];
    if (regcomp(&regexCompiled, "^([0-9]+)-([0-9]+) ([a-z]): (.*)$", REG_EXTENDED))
    {
        perror("Error compiling regex.");
        exit(1);
    }
    Line *lines = calloc(MAX_COUNT, sizeof(Line));
    int count = 0, group;
    size_t lineLength;
    char *line = NULL, *cursor = NULL;
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        int first, second;
        char letter;
        char *password = malloc(32);
        while (!regexec(&regexCompiled, cursor, MAX_COUNT, groupArray, 0))
        {
            for (group = 0; group <= 4 && groupArray[group].rm_so != -1; group++)
            {
                char cursorCopy[strlen(cursor) + 1];
                strcpy(cursorCopy, cursor);
                cursorCopy[groupArray[group].rm_eo] = 0;
                switch (group)
                {
                case 1:
                    first = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    second = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 3:
                    letter = cursorCopy[groupArray[group].rm_so];
                    break;
                case 4:
                    strcpy(password, cursorCopy + groupArray[group].rm_so);
                    break;
                }
            }
            cursor += groupArray[0].rm_eo;
        }
        lines[count++] = (Line){first, second, letter, password};
    }
    regfree(&regexCompiled);
    fclose(file);
    return (Input){lines, count};
}

void freeInput(Input input)
{
    Line *lines = input.lines;
    while (input.count--)
        free((lines++)->password);
    free(input.lines);
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

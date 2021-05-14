#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

#define MAX_COUNT 2048

typedef struct
{
    int sides[3];
} Triangle;

typedef struct
{
    Triangle *triangles;
    int count;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int isPossibleTriangle(int sideA, int sideB, int sideC)
{
    return sideA < (sideB + sideC) && sideB < (sideA + sideC) && sideC < (sideA + sideB);
}

int part1(Input input)
{
    int valid = 0;
    while (input.count--)
    {
        valid += isPossibleTriangle(input.triangles->sides[0], input.triangles->sides[1], input.triangles->sides[2]);
        input.triangles++;
    }
    return valid;
}

int part2(Input input)
{
    int valid = 0;
    for (int index = 0; index < input.count; index++)
        valid += isPossibleTriangle(
            input.triangles[(index / 3) * 3].sides[index % 3],
            input.triangles[(index / 3) * 3 + 1].sides[index % 3],
            input.triangles[(index / 3) * 3 + 2].sides[index % 3]);
    return valid;
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
    regex_t regexCompiled;
    regmatch_t groupArray[MAX_COUNT];
    if (regcomp(&regexCompiled, "([0-9]+) +([0-9]+) +([0-9]+)", REG_EXTENDED))
    {
        perror("Error compiling regex.");
        exit(1);
    }
    size_t lineLength;
    Triangle *triangles = calloc(MAX_COUNT, sizeof(Triangle));
    int count = 0, group, a, b, c;
    char *line = NULL, *cursor = NULL;
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        while (!regexec(&regexCompiled, cursor, MAX_COUNT, groupArray, 0))
        {
            for (group = 0; group <= 3 && groupArray[group].rm_so != -1; group++)
            {
                char cursorCopy[strlen(cursor) + 1];
                strcpy(cursorCopy, cursor);
                cursorCopy[groupArray[group].rm_eo] = 0;
                switch (group)
                {
                case 1:
                    a = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    b = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 3:
                    c = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                }
            }
            cursor += groupArray[0].rm_eo;
        }
        triangles[count++] = (Triangle){{a, b, c}};
    }
    fclose(file);
    return (Input){triangles, count};
}

void freeInput(Input input)
{
    free(input.triangles);
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
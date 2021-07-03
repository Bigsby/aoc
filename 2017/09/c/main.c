#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef char *Input;
typedef struct
{
    int part1;
    int part2;
} Results;

#define GROUP_START '{'
#define GROUP_END '}'
#define GARBAGE_START '<'
#define GARBAGE_END '>'
#define ESCAPE '!'

Results solve(Input input)
{
    int groupScore = 0, garbageCount = 0, depth = 0, inGarbage = 0, escape = 0;
    char c;
    while (c = *(input++))
    {
        if (escape)
            escape = 0;
        else if (inGarbage)
        {
            if (c == ESCAPE)
                escape = 1;
            else if (c == GARBAGE_END)
                inGarbage = 0;
            else
                garbageCount++;
        }
        else if (c == GARBAGE_START)
            inGarbage = 1;
        else if (c == GROUP_START)
            depth++;
        else if (c == GROUP_END)
            groupScore += depth--;
    }
    return (Results){groupScore, garbageCount};
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
    return content;
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

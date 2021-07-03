#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef char *Input;
typedef struct
{
    long part1;
    long part2;
} Results;

typedef enum {
    PRIOR = 0,
    LENGTH = 1,
    REPEATS = 2,
    DATA = 3
} CrawlPhase;

long getLength(char *data, int start, int end, int recursive)
{
    int priorLength = 0, length = 0, repeats = 0;
    CrawlPhase phase = PRIOR;
    char c;
    while (start < end)
    {
        c = data[start];
        switch (phase)
        {
            case PRIOR:
                if (c == '(')
                    phase++;
                else
                    priorLength++;
                break;
            case LENGTH:
                if (c == 'x')
                    phase++;
                else
                    length = length * 10 + c - '0';
                break;
            case REPEATS:
                if (c == ')')
                    phase++;
                else
                    repeats = repeats * 10 + c - '0';
                break;
            case DATA:
                return priorLength + repeats * (recursive ? getLength(data, start, start + length, 1) : length) + getLength(data, start + length, end, recursive);
        }
        start++;
    }
    return priorLength;
}

Results solve(Input input)
{
    int end = strlen(input) - 1;
    return (Results){ getLength(input, 0, end, 0), getLength(input, 0, end, 1)};
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

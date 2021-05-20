#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct
{
    int start, end;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int isPasswordValid(int password, int check2)
{
    int previous = 9, current, counts[10], index = 10, hasTwo = !check2, hasGreaterThanOne = 0;
    for (index = 0; index < 10; index++)
        counts[index] = 0;
    for (; password && index; --index, password /= 10)
    {
        current = password % 10;
        if (previous < current)
            return 0;
        counts[current]++;
        previous = current;
    }
    for (index = 0; index < 10; index++)
    {
        hasTwo |= counts[index] == 2;
        hasGreaterThanOne |= counts[index] > 1;
    }
    return hasTwo && hasGreaterThanOne;
}

int getValidPasswordCount(Input limits, int check2)
{
    int count = 0;
    for (int password = limits.start; password < limits.end; password++)
        count += isPasswordValid(password, check2);
    return count;
}

Results solve(Input input)
{
    return (Results){getValidPasswordCount(input, 0), getValidPasswordCount(input, 1)};
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
    char contents[length + 1];
    fread(contents, length, 1, file);
    int start, end;
    sscanf(contents, "%d-%d", &start, &end);
    fclose(file);
    return (Input){
        start,
        end};
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
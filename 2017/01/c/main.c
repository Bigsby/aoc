#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct
{
    int *numbers;
    int size;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int getCount(Input input, int indexOffset)
{
    int count = 0;
    for (int index = 0; index < input.size; index++)
        if (input.numbers[index] == input.numbers[(index + indexOffset) % input.size])
            count += input.numbers[index];
    return count;
}

Results solve(Input input)
{
    return (Results){
        getCount(input, input.size - 1),
        getCount(input, input.size / 2)};
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
    int length = ftell(file);
    rewind(file);
    int *numbers = calloc(length, sizeof(int));
    int *current = numbers;
    int c;
    while ((c = getc(file)) != EOF)
        if (c >= '0' && c <= '9')
            *current++ = c - '0';
        else
            length--;
    fclose(file);
    return (Input){numbers, length};
}

void freeInput(Input input)
{
    free(input.numbers);
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
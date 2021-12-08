#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct {
    int *jumps, count, size;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int part1(int offset)
{
    return 1;
}

int part2(int offset)
{
    return offset < 3 ? 1 : -1;
}

int doJumps(Input input, int (*newJumpFunc)(int))
{
    int *jumps = calloc(input.count, sizeof(int));
    memcpy(jumps, input.jumps, input.count * (sizeof(int)));
    int index = 0, count = 0, offset, nextIndex;
    while (index >= 0 && index < input.count)
    {
        count++;
        offset = jumps[index];
        nextIndex = index + offset;
        jumps[index] = offset + newJumpFunc(offset);
        index = nextIndex;
    }
    free(jumps);
    return count;
}

Results solve(Input input)
{
    return (Results){doJumps(input, &part1), doJumps(input, &part2)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int jump)
{
    if (input->count == input->size)
    {
        input->size += INPUT_INCREMENT;
        input->jumps = realloc(input->jumps, input->size * sizeof(int));
    }
    input->jumps[input->count++] = jump;
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
        calloc(INPUT_INCREMENT, sizeof(int)),
        0,
        INPUT_INCREMENT
    };
    char *line = NULL;
    size_t lineLength;
    while (getline(&line, &lineLength, file) != EOF)
        addToInput(&input, atoi(line));
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.jumps);
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

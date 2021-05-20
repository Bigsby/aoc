#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct
{
    int *changes;
    int count;
    int size;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int part1(Input input)
{
    int total = 0;
    while (input.count--)
        total += *(input.changes++);
    return total;
}

typedef struct BinaryNode
{
    int value;
    struct BinaryNode *lesser;
    struct BinaryNode *greater;
} BinaryNode;

struct BinaryNode *insert(BinaryNode *node, int value, int *inserted)
{
    if (node == NULL)
    {
        node = malloc(sizeof(BinaryNode));
        node->value = value;
        node->lesser = node->greater = NULL;
        *inserted = 1;
    }
    else if (node->value == value)
        *inserted = 0;
    else if (node->value < value)
        node->lesser = insert(node->lesser, value, inserted);
    else if (node->value > value)
        node->greater = insert(node->greater, value, inserted);
    return node;
}

void freeTree(BinaryNode *node)
{
    if (node != NULL)
    {
        freeTree(node->lesser);
        freeTree(node->greater);
        free(node);
    }
}

int part2(Input input)
{
    int frequency = 0;
    BinaryNode *previous = NULL;
    int inserted = 0;
    int index = 0;
    previous = insert(previous, frequency, &inserted);
    while (inserted)
    {
        frequency += input.changes[index];
        index = (index + 1) % input.count;
        previous = insert(previous, frequency, &inserted);
    }
    freeTree(previous);
    return frequency;
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
}

void addToInput(Input *input, int change)
{
    if (input->count == input->size)
    {
        int *oldChanges = input->changes;
        int *newChanges = realloc(oldChanges, (input->size + 10) * (sizeof(int)));
        input->changes = newChanges;
        input->size += 10;
    }
    input->changes[input->count++] = change;
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
    char *line = NULL;
    size_t len = 0;
    size_t read;
    Input input = {
        malloc(10 * sizeof(int)),
        0,
        10
    };
    while (getline(&line, &len, file) != EOF)
        addToInput(&input, atoi(line));
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.changes);
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
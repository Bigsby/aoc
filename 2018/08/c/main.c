#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct {
    int count, capacity, *data;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct Node {
    int childrenCount;
    struct Node *children;
    int metadataCount;
    int *metadata;
} Node;

Node readNode(Input *input)
{
    Node node;
    node.childrenCount = *(input->data++);
    node.metadataCount = *(input->data++);
    node.children = malloc(node.childrenCount * sizeof(Node));
    node.metadata = malloc(node.metadataCount * sizeof(int));
    for (int childIndex = 0; childIndex < node.childrenCount; childIndex++)
        node.children[childIndex] = readNode(input);
    for (int metadataIndex = 0; metadataIndex < node.metadataCount; metadataIndex++)
        node.metadata[metadataIndex] = *(input->data++);
    return node;
}

int getMetadataSum(Node node)
{
    int total = 0, index;
    for (index = 0; index < node.metadataCount; index++)
        total += node.metadata[index];
    for (index = 0; index < node.childrenCount; index++)
        total += getMetadataSum(node.children[index]);
    return total;
}

int getValue(Node node)
{
    int total = 0, index, childIndex;
    if (node.childrenCount == 0)
        for (index = 0; index < node.metadataCount; index++)
            total += node.metadata[index];
    else 
        for (index = 0; index < node.metadataCount; index++)
        {
            childIndex = node.metadata[index];
            if (childIndex > 0 && childIndex <= node.childrenCount)
                total += getValue(node.children[childIndex - 1]);
        }
    return total;
}

Results solve(Input input)
{
    Node root = readNode(&input);
    return (Results){getMetadataSum(root), getValue(root)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int value)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        int *oldData = input->data;
        int *newData = realloc(oldData, input->capacity * sizeof(int));
        input->data = newData;
    }
    input->data[input->count++] = value;
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
    char content[length];
    fread(content, 1, length, file);
    Input input = {
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(int))
    };
    char *value = strtok(content, " ");
    while (value != NULL)
    {
        addToInput(&input, atoi(value));
        value = strtok(NULL, " ");
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.data);
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

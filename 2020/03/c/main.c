#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <complex.h>

typedef double complex Lattice;

typedef struct TreesNode
{
    int x, y;
    struct TreesNode *left, *right;
} TreesNode;

typedef struct
{
    TreesNode *trees;
    int width, height;
} Input;

#define PART2_FORMAT "%ld"
typedef struct
{
    long part1;
    long part2;
} Results;

int comparePositions(int aX, int aY, int bX, int bY)
{
    if (aY > bY)
        return 1;
    if (aY < bY)
        return -1;
    if (aX > bX)
        return 1;
    if (aX < bX)
        return -1;
    return 0;
}

TreesNode *addTree(TreesNode *node, int x, int y)
{
    int compare;
    if (node == NULL)
    {
        node = malloc(sizeof(TreesNode));
        node->x = x;
        node->y = y;
        node->left = node->right = NULL;
    }
    else if ((compare = comparePositions(node->x, node->y, x, y)) == 1)
        node->left = addTree(node->left, x, y);
    else if (compare == -1)
        node->right = addTree(node->right, x, y);
    return node;
}

int containsTree(TreesNode *node, int x, int y)
{
    if (node == NULL)
        return 0;
    int compare = comparePositions(node->x, node->y, x, y);
    if (compare == 0)
        return 1;
    return compare == 1 ? containsTree(node->left, x, y) : containsTree(node->right, x, y);
}

long calculateTrees(Input input, Lattice step)
{
    Lattice position = 0;
    long treeCount = 0L;
    while (cimag(position) < input.height)
    {
        treeCount += containsTree(input.trees, (int)creal(position) % input.width, cimag(position));
        position += step;
    }
    return treeCount;
}

const Lattice steps[] = {
    1 + I,
    3 + I,
    5 + I,
    7 + I,
    1 + 2 * I};
long part2(Input input)
{
    long product = 1UL, index;
    for (index = 0; index < 5; index++)
        product *= calculateTrees(input, steps[index]);
    return product;
}

Results solve(Input input)
{
    return (Results){calculateTrees(input, 3 + I), part2(input)};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    size_t lineLength;
    TreesNode *trees = NULL;
    char *line, *cursor, c;
    int width = 0, height = 0, x;
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        x = 0;
        while (1)
        {
            if (*cursor == '#')
                trees = addTree(trees, x, height);
            else if (*cursor != '.')
                break;
            cursor++;
            x++;
        }
        if (width == 0)
            width = x;
        height++;
    }
    fclose(file);
    return (Input){trees, width, height};
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
    printf("P2: "
    #ifdef PART2_FORMAT
        PART2_FORMAT
    #else
        "%d"
    #endif
     "\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}
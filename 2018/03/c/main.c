#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

#define MAX_COUNT 2048

typedef struct
{
    int id;
    int left;
    int top;
    int width;
    int height;
} Claim;

typedef struct
{
    Claim *claims;
    int count;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct
{
    int x, y;
} Key;
typedef int Value;
#define INITIAL_VALUE 0
#define UNDEFINED_VALUE -1

typedef struct BinaryNode
{
    Key key;
    Value value;
    struct BinaryNode *left;
    struct BinaryNode *right;
} BinaryNode;

int compareKeys(Key a, Key b)
{
    if (a.y > b.y)
        return 1;
    if (a.y < b.y)
        return -1;
    if (a.x > b.x)
        return 1;
    if (a.x < b.x)
        return -1;
    return 0;
}

Value getNewValue(Value previousValue, Value newValue)
{
    return previousValue + newValue;
}

BinaryNode *setBinaryNode(BinaryNode *node, Key key, Value value)
{
    int compare;
    if (node == NULL)
    {
        node = malloc(sizeof(BinaryNode));
        node->key = key;
        node->value = getNewValue(INITIAL_VALUE, value);
        node->left = node->right = NULL;
    }
    else if ((compare = compareKeys(node->key, key)) == 0)
        node->value = getNewValue(node->value, value);
    else if (compare < 0)
        node->left = setBinaryNode(node->left, key, value);
    else
        node->right = setBinaryNode(node->right, key, value);
    return node;
}

Value getBinaryNodeValue(BinaryNode *node, Key key)
{
    int compare;
    if (node == NULL)
        return UNDEFINED_VALUE;
    if ((compare = compareKeys(node->key, key)) == 0)
        return node->value;
    if (compare < 0)
        return getBinaryNodeValue(node->left, key);
    return getBinaryNodeValue(node->right, key);
}

BinaryNode *buildPointTree(Input input)
{
    BinaryNode *root = NULL;
    int x, y;
    while (input.count--)
    {
        for (x = input.claims->left; x < input.claims->left + input.claims->width; x++)
            for (y = input.claims->top; y < input.claims->top + input.claims->height; y++)
                root = setBinaryNode(root, (Key){x, y}, 1);
        input.claims++;
    }
    return root;
}

int part1(BinaryNode *pointNode)
{
    if (pointNode == NULL)
        return 0;
    return (pointNode->value > 1) + part1(pointNode->left) + part1(pointNode->right);
}

int allCountsOne(int left, int top, int width, int height, BinaryNode *pointTree)
{
    int x, y;
    for (x = left; x < left + width; x++)
        for (y = top; y < top + height; y++)
            if (getBinaryNodeValue(pointTree, (Key){x, y}) != 1)
                return 0;
    return 1;
}

int part2(Input input, BinaryNode *pointTree)
{
    while (input.count--)
    {
        if (allCountsOne(input.claims->left, input.claims->top, input.claims->width, input.claims->height, pointTree))
            return input.claims->id;
        input.claims++;
    }
    return -1;
}

Results solve(Input input)
{
    BinaryNode *pointTree = buildPointTree(input);
    return (Results){part1(pointTree), part2(input, pointTree)};
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
    if (regcomp(&regexCompiled, "^#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)", REG_EXTENDED))
    {
        perror("Error compiling regex.");
        exit(1);
    };
    Claim *claims = calloc(MAX_COUNT, sizeof(Claim));
    int count = 0, group, id, left, top, width, height;
    char *line = NULL, *cursor = NULL;
    size_t lineLength;
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        while (!regexec(&regexCompiled, cursor, MAX_COUNT, groupArray, 0))
        {
            for (group = 0; group <= 5 && groupArray[group].rm_so != -1; group++)
            {
                char cursorCopy[strlen(cursor) + 1];
                strcpy(cursorCopy, cursor);
                cursorCopy[groupArray[group].rm_eo] = 0;
                switch (group)
                {
                case 1:
                    id = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    left = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 3:
                    top = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 4:
                    width = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 5:
                    height = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                }
            }
            cursor += groupArray[0].rm_eo;
        }
        claims[count++] = (Claim){id, left, top, width, height};
    }

    fclose(file);
    return (Input){claims, count};
}

void freeInput(Input input)
{
    free(input.claims);
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
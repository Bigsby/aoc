#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct {
    int x1, y1, x2, y2;
} Line;

typedef struct {
    Line *lines;
    int count, capacity;
} Input;

typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct DiagramNode {
    int x, y, count;
    struct DiagramNode *left;
    struct DiagramNode *right;
} DiagramNode;

int compareCoordinates(int x1, int y1, int x2, int y2)
{
    if (x1 > x2)
        return 1;
    if (x1 < x2)
        return -1;
    if (y1 > y2)
        return 1;
    if (y1 < y2)
        return -1;
    return 0;
}

DiagramNode *addToDiagram(DiagramNode *node, int x, int y)
{
    if (node == NULL)
    {
        node = malloc(sizeof(DiagramNode));
        node->x = x;
        node->y = y;
        node->count = 1;
        node->left = node->right = NULL;
    } else {
        int compare = compareCoordinates(node->x, node->y, x, y);
        if (compare == 0)
            node->count++;
        else if (compare < 0)
            node->left = addToDiagram(node->left, x, y);
        else
            node->right = addToDiagram(node->right, x, y);
    }
    return node;
}

int getDiagramCount(DiagramNode *node)
{
    if (node != NULL)
        return (node->count > 1) + getDiagramCount(node->left) + getDiagramCount(node->right);
    return 0;
}

int getCoveredCount(Input input, int diagonals)
{
    DiagramNode *root = NULL;
    while (input.count--)
    {
        int x1 = input.lines->x1;
        int y1 = input.lines->y1;
        int x2 = input.lines->x2;
        int y2 = input.lines->y2;
        input.lines++;
        if (x1 == x2)
            for (int y = y1 < y2 ? y1 : y2; y < (y1 > y2 ? y1 : y2) + 1; y++)
                root = addToDiagram(root, x1, y);
        else if (y1 == y2)
            for (int x = x1 < x2 ? x1 : x2; x < (x1 > x2 ? x1 : x2) + 1; x++)
                root = addToDiagram(root, x, y1);
        else if (diagonals)
        {
            int xDirection = x2 > x1 ? 1 : -1;
            int yDirection = y2 > y1 ? 1 : -1;
            int count = abs(x2 - x1) + 1;
            for (int xy = 0; xy < count; xy++)
                root = addToDiagram(root, x1 + xy * xDirection, y1 + xy * yDirection);
        }
    }
    return getDiagramCount(root);
}

Results solve(Input input)
{
    return (Results){getCoveredCount(input, 0), getCoveredCount(input, 1)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int x1, int y1, int x2, int y2)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->lines = realloc(input->lines, input->capacity * sizeof(Line));
    }
    input->lines[input->count++] = (Line) { x1, y1, x2, y2 };
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
        malloc(sizeof(Line) * INPUT_INCREMENT),
        0, INPUT_INCREMENT
    };
    size_t len;
    char *line = NULL;
    int x1, y1, x2, y2;
    while (getline(&line, &len, file) != EOF)
        if (sscanf(line, "%d,%d -> %d,%d", &x1, &y1, &x2, &y2) == 4)
            addToInput(&input, x1, y1, x2, y2);
        else
        {
            perror("Bad line: ");
            perror(line);
            exit(1);
        }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.lines);
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

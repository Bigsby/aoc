#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <complex.h>
#include <math.h>

typedef double complex Point;
typedef struct {
    int direction;
    int coordinate;
} Folding;
typedef struct {
    Point *points;
    int pointsSize, pointsCapacity;
    Folding *foldings;
    int foldingsSize, foldingsCapacity;
} Input;
typedef struct
{
    int part1;
    char *part2;
} Results;

typedef struct {
    Point *points;
    int size, capacity;
} Paper;

#define A \
    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b11110 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5)
#define B \
    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b11100 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b11100 << CHARACTER_WIDTH * 5)
#define C \
    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5)
#define D \
    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b11100 << CHARACTER_WIDTH * 5)
#define E \
    (0b11110 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b11100 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b11110 << CHARACTER_WIDTH * 5)
#define F \
    (0b11110 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b11100 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b10000 << CHARACTER_WIDTH * 5)
#define G \
    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b10110 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01110 << CHARACTER_WIDTH * 5)
#define H \
    (0b10010 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b11110 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5)
#define LETTER_I \
    (0b01110 << CHARACTER_WIDTH * 0) + \
    (0b00100 << CHARACTER_WIDTH * 1) + \
    (0b00100 << CHARACTER_WIDTH * 2) + \
    (0b00100 << CHARACTER_WIDTH * 3) + \
    (0b00100 << CHARACTER_WIDTH * 4) + \
    (0b01110 << CHARACTER_WIDTH * 5)
#define J \
    (0b00110 << CHARACTER_WIDTH * 0) + \
    (0b00010 << CHARACTER_WIDTH * 1) + \
    (0b00010 << CHARACTER_WIDTH * 2) + \
    (0b00010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5)
#define K \
    (0b10010 << CHARACTER_WIDTH * 0) + \
    (0b10100 << CHARACTER_WIDTH * 1) + \
    (0b11000 << CHARACTER_WIDTH * 2) + \
    (0b10100 << CHARACTER_WIDTH * 3) + \
    (0b10100 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5)
#define L \
    (0b10000 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b11110 << CHARACTER_WIDTH * 5)
#define M 0
#define N 0
#define O \
    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5)
#define P \
    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b11100 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b10000 << CHARACTER_WIDTH * 5)
#define Q 0
#define R \
    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b11100 << CHARACTER_WIDTH * 3) + \
    (0b10100 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5)
#define S \
    (0b01110 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b01100 << CHARACTER_WIDTH * 3) + \
    (0b00010 << CHARACTER_WIDTH * 4) + \
    (0b11100 << CHARACTER_WIDTH * 5)
#define T 0
#define U \
    (0b10010 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5)
#define V 0
#define W 0
#define X 0
#define Y \
    (0b10001 << CHARACTER_WIDTH * 0) + \
    (0b10001 << CHARACTER_WIDTH * 1) + \
    (0b01010 << CHARACTER_WIDTH * 2) + \
    (0b00100 << CHARACTER_WIDTH * 3) + \
    (0b00100 << CHARACTER_WIDTH * 4) + \
    (0b00100 << CHARACTER_WIDTH * 5)
#define Z \
    (0b11110 << CHARACTER_WIDTH * 0) + \
    (0b00010 << CHARACTER_WIDTH * 1) + \
    (0b00100 << CHARACTER_WIDTH * 2) + \
    (0b01000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b11110 << CHARACTER_WIDTH * 5)

#define SCREEN_WIDTH 40
#define SCREEN_HEIGHT 6
#define CHARACTER_WIDTH 5

const int LETTERS[] = { A,B,C,D,E,F,G,H,LETTER_I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z };

char getLetter(int value)
{
    for (int index = 0; index < 26; index++)
        if (LETTERS[index] == value)
            return 'A' + index;
    perror("Unknow character");
    exit(1);
}

int inPaper(Paper paper, Point point)
{
    for (int index = 0; index < paper.size; index++)
        if (paper.points[index] == point)
            return 1;
    return 0;
}

char *getCode(Paper paper)
{
    int paperValue, x, y;
    char *code = calloc((SCREEN_WIDTH / CHARACTER_WIDTH) + 1, 1);
    for (int index = 0; index < SCREEN_WIDTH / CHARACTER_WIDTH; index++)
    {
        paperValue = 0;
        for (x = 0; x < CHARACTER_WIDTH; x++)
            for (y = 0; y < SCREEN_HEIGHT; y++)
                paperValue += inPaper(paper, CHARACTER_WIDTH * index + x + y * I) * ((int)pow(2, CHARACTER_WIDTH - 1 - x) << (y * CHARACTER_WIDTH));
        code[index] = getLetter(paperValue);
    }
    return code;
}

#define PAPER_INCREMENT 10
void addToPaper(Paper *paper, Point point)
{
    for (int index = 0; index < paper->size; index++)
        if (paper->points[index] == point)
            return;
    if (paper->size == paper->capacity)
        paper->points = realloc(paper->points, (paper->capacity += PAPER_INCREMENT) * sizeof(Point));
    paper->points[paper->size++] = point;
}

int includeX(Point point)
{
    return (int)creal(point);
}

int includeY(Point point)
{
    return (int)cimag(point);
}

Point newPointX(Point point, int coordinate)
{
    return 2 * coordinate - creal(point) + cimag(point) * I;
}

Point newPointY(Point point, int coordinate)
{
    return creal(point) + I * (2 * coordinate - cimag(point));
}

Paper fold(Paper paper, Folding folding)
{
    Point *points = paper.points;
    int (*includeFunc)(Point) = folding.direction ? includeX : includeY;
    Point (*newPointFunc)(Point, int) = folding.direction ? newPointX : newPointY;
    Paper newPaper = {
        malloc(PAPER_INCREMENT * sizeof(Point)),
        0, PAPER_INCREMENT
    };
    while (paper.size--)
    {
        Point point = *points++;
        addToPaper(&newPaper, includeFunc(point) < folding.coordinate ? point : newPointFunc(point, folding.coordinate));
    }
    free(paper.points);
    return newPaper;
}

Results solve(Input input)
{
    int part1 = 0;
    Paper paper = {
        input.points,
        input.pointsSize,
        input.pointsCapacity
    };
    while (input.foldingsSize--)
    {
        paper = fold(paper, *input.foldings++);
        if (!part1)
            part1 = paper.size;
    }
    return (Results){part1, getCode(paper)};
}

#define INPUT_INCREMENT 10
void addPointToInput(Input *input, int x, int y)
{
    if (input->pointsSize == input->pointsCapacity)
        input->points = realloc(input->points, (input->pointsCapacity += INPUT_INCREMENT) * sizeof(Point));
    input->points[input->pointsSize++] = x + y * I;
}

void addFoldingToInput(Input *input, int direction, int coordinate)
{
    if (input->foldingsSize == input->foldingsCapacity)
        input->foldings = realloc(input->foldings, (input->foldingsCapacity += INPUT_INCREMENT) * sizeof(Folding));
    input->foldings[input->foldingsSize++] = (Folding){ direction, coordinate };
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
        malloc(INPUT_INCREMENT * sizeof(Point)),
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(Folding)),
        0, INPUT_INCREMENT
    };
    char *line = NULL;
    size_t len;
    int foldings = 0;
    char direction[2];
    int coordinate, x, y;
    while (getline(&line, &len, file) != EOF)
    {
        if (line[0] == '\n')
        {
            foldings = 1;
            continue;
        }
        if (foldings)
        {
            sscanf(line, "fold along %[^=]=%d", direction, &coordinate);
            addFoldingToInput(&input, direction[0] == 'x', coordinate);
        } else
        {
            sscanf(line, "%d,%d", &x, &y);
            addPointToInput(&input, x, y);
        }
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.foldings);
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
    printf("P2: %s\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}

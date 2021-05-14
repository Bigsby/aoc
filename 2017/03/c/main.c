#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>
#include <complex.h>

typedef double complex Lattice;

typedef int Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int part1(Input targetNumber)
{
    int side = (int)floor(sqrt(targetNumber)) + 1;
    int pastLastSquare = targetNumber - pow((side - 1), 2);
    int halfSide = side / 2;
    if (pastLastSquare >= side)
        pastLastSquare -= side;
    int offsetToMiddle = abs(halfSide - pastLastSquare);
    return halfSide + offsetToMiddle;
}

typedef struct
{
    Lattice key;
    int value;
} GridItem;

typedef struct
{
    GridItem *items;
    int count;
    int size;
} Grid;

void addItem(Grid *grid, Lattice lattice, int value)
{
    if (grid->size == grid->count)
    {
        GridItem *oldItems = grid->items;
        GridItem *newItems = realloc(oldItems, sizeof(GridItem) * (grid->size + 10));
        grid->items = newItems;
        grid->size += 10;
    }
    grid->items[grid->count++] = (GridItem){lattice, value};
}

Grid createGrid()
{
    return (Grid){
        calloc(10, sizeof(GridItem)),
        0,
        10};
}

int getValueForPosition(Grid *grid, Lattice position)
{
    int count = grid->count;
    GridItem *items = grid->items;
    while (count--)
    {
        if (items->key == position)
            return items->value;
        items++;
    }
    return 0;
}

const Lattice DIRECTIONS[8] = {
    -1 - I, -I, 1 - I,
    -1, 1,
    -1 + I, I, 1 + I};

int getSumForNeighbors(Grid *grid, Lattice position)
{
    int total = 0;
    for (int index = 0; index < 8; index++)
        total += getValueForPosition(grid, position + DIRECTIONS[index]);
    return total;
}

int part2(Input target)
{
    Grid grid = createGrid();
    Lattice position = 0;
    Lattice direction = 1;
    addItem(&grid, position, 1);
    int movesInDirection = 1, move, directionMoves, newValue;
    while (1)
    {
        for (move = 0; move < 2; move++)
        {
            direction *= I;
            for (directionMoves = 0; directionMoves < movesInDirection; directionMoves++)
            {
                position += direction;
                newValue = getSumForNeighbors(&grid, position);
                if (newValue > target)
                {
                    free(grid.items);
                    return newValue;
                }
                addItem(&grid, position, newValue);
            }
        }
        movesInDirection++;
    }
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
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
    int targetNumber = atoi(content);
    fclose(file);
    return targetNumber;
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
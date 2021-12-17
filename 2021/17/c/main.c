#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>

typedef struct {
    int x1, x2, y1, y2;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int isDirectionValid(Input targetArea, int directionX, int directionY)
{
    int currentX = 0, currentY = 0;
    while (currentX <= targetArea.x2 && currentY >= targetArea.y1)
    {
        currentX += directionX;
        currentY += directionY;
        if (currentX >= targetArea.x1 && currentX <= targetArea.x2 && currentY >= targetArea.y1 && currentY <= targetArea.y2)
            return 1;
        directionX = directionX == 0 ? 0 : directionX - 1;
        directionY -= 1;
    }
    return 0;
}

int countValidInRange(Input targetArea, int xStart, int xEnd, int yStart, int yEnd)
{
    int count = 0;
    for (int x = xStart; x < xEnd; x++)
        for (int y = yStart; y < yEnd; y++)
            count += isDirectionValid(targetArea, x, y);
    return count;
}

Results solve(Input targetArea)
{
    int yDirection = -targetArea.y1 - 1;
    int validDirectionCount = (targetArea.x2 - targetArea.x1 + 1) * (-targetArea.y1 + targetArea.y2 + 1);
    validDirectionCount += countValidInRange(
        targetArea,
        ceil((sqrt(8 * targetArea.x1 + 1) -1) / 2), targetArea.x2 / 2 + 2,
        targetArea.y2 + 1, -targetArea.y1
    );
    return (Results){(yDirection * (yDirection + 1)) / 2, validDirectionCount};
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
    int x1, x2, y1, y2;
    sscanf(content, "target area: x=%d..%d, y=%d..%d", &x1, &x2, &y1, &y2);
    fclose(file);
    return (Input) { x1, x2, y1, y2 };
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

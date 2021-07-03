#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct {
    int elvesCount, lastMarble;
} Input;
typedef struct
{
    long part1;
    long part2;
} Results;

typedef struct {
    int previous, next;
} Marble;

typedef struct {
    int current;
    Marble *marbles;
} Circle;

long max(long *scores, int size)
{
    long result = 0;
    while (size--)
    {
        result = *scores > result ? *scores : result;
        scores++;
    }
    return result;
}

void printCircle(Circle circle)
{
    int marble = 0;
    do
    {
        if (marble == circle.current)
            printf("(");
        printf("%d", marble);
        if (marble == circle.current)
            printf(")");
        printf(" ");
        marble = circle.marbles[marble].next;
    } while (marble);
}

Results solve(Input input)
{
    long *scores = calloc(input.elvesCount, sizeof(long));
    Circle circle = {0, malloc(input.lastMarble * 100 * sizeof(Marble))};
    circle.marbles[0] = (Marble){0, 0};
    long part1Score = 0, rotate;
    for (int nextMarble = 1; nextMarble <= input.lastMarble * 100; nextMarble++)
    {
        if (nextMarble == input.lastMarble)
            part1Score = max(scores, input.elvesCount);
        if (nextMarble % 23)
        {
            circle.current = circle.marbles[circle.current].next;
            circle.marbles[nextMarble] = (Marble){circle.current, circle.marbles[circle.current].next};
            circle.marbles[circle.marbles[circle.current].next].previous = nextMarble;
            circle.marbles[circle.current].next = nextMarble;
            circle.current = nextMarble;
        }
        else
        {
            for (rotate = 0; rotate < 7; rotate++)
                circle.current = circle.marbles[circle.current].previous;
            scores[nextMarble % input.elvesCount] += nextMarble + circle.current;
            circle.marbles[circle.marbles[circle.current].previous].next = circle.marbles[circle.current].next;
            circle.current = circle.marbles[circle.current].next;
        }
    }
    return (Results){part1Score, max(scores, input.elvesCount)};
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
    int elvesCount, lastMarble;
    sscanf(content, "%d players; last marble is worth %d points", &elvesCount, &lastMarble);
    fclose(file);
    return (Input) {elvesCount, lastMarble};
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
    printf("P2: %ld\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct
{
    int width;
    int length;
    int height;
} Dimensions;

typedef struct
{
    Dimensions *dimensions;
    int count;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define MIN_THREE(a, b, c) MIN(MIN(a, b), c)

int part1(Input input)
{
    int totalPaper = 0;
    while (input.count--)
    {
        int wl = input.dimensions->width * input.dimensions->length;
        int wh = input.dimensions->width * input.dimensions->height;
        int hl = input.dimensions->height * input.dimensions->length;
        int smallest = MIN_THREE(wl, wh, hl);
        totalPaper += 2 * (wl + wh + hl) + smallest;
        input.dimensions++;
    }
    return totalPaper;
}

int part2(Input input)
{
    int totalRibbon = 0;
    int height, length, width;
    int smaller1, smaller2, intermediate;
    while (input.count--)
    {
        height = input.dimensions->height;
        length = input.dimensions->length;
        width = input.dimensions->width;
        if (height > length)
        {
            smaller1 = length;
            intermediate = height;
        }
        else
        {
            smaller1 = height;
            intermediate = length;
        }
        smaller2 = intermediate > width ? width : intermediate;
        totalRibbon += 2 * (smaller1 + smaller2) + height * length * width;
        input.dimensions++;
    }
    return totalRibbon;
}

Results solve(Input dimensions)
{
    return (Results){part1(dimensions), part2(dimensions)};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    Dimensions *dimensions = calloc(1024, sizeof(Dimensions));
    Dimensions *current = dimensions;
    size_t len = 0;
    char *line;
    int width, length, height;
    int count = 0;
    while (getline(&line, &len, file) != EOF)
    {
        sscanf(line, "%dx%dx%d", &width, &length, &height);
        *current++ = (Dimensions){
            width, length, height};
        count++;
    }
    fclose(file);
    return (Input){dimensions, count};
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
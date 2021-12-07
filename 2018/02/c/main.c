#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct
{
    char **ids;
    size_t length;
} Input;

typedef struct
{
    int part1;
    char *part2;
} Results;

int part1(Input input)
{
    int twiceCount = 0, thriceCount = 0, index = 0, cIndex;
    int counts[26];
    char *id;
    char c;
    while (input.length--)
    {
        id = input.ids[index];
        for (cIndex = 0; cIndex < 26; cIndex++)
            counts[cIndex] = 0;
        cIndex = 0;
        while (c = id[cIndex++])
            counts[c - 'a']++;
        int hasTwos = 0, hasThrees = 0;
        for (cIndex = 0; cIndex < 26; cIndex++)
        {
            hasTwos |= counts[cIndex] == 2;
            hasThrees |= counts[cIndex] == 3;
        }
        twiceCount += hasTwos;
        thriceCount += hasThrees;
        index++;
    }
    return twiceCount * thriceCount;
}

char *part2(Input input)
{
    int thisIndex, otherIndex, cIndex, differenceCount, differenceIndex;
    char *thisId, *otherId;
    for (thisIndex = 0; thisIndex < input.length; thisIndex++)
    {
        thisId = input.ids[thisIndex];
        for (otherIndex = thisIndex + 1; otherIndex < input.length; otherIndex++)
        {
            differenceCount = 0;
            differenceIndex = 0;
            otherId = input.ids[otherIndex];
            for (cIndex = 0; cIndex < strlen(thisId); cIndex++)
                if (thisId[cIndex] != otherId[cIndex])
                {
                    differenceCount++;
                    differenceIndex = cIndex;
                }
            if (differenceCount == 1)
            {
                thisId[differenceIndex] = 0;
                otherId += differenceIndex + 1;
                strcat(thisId, otherId);
                return thisId;
            }
        }
    }
    return NULL;
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
    char **ids = calloc(256, sizeof(char *));
    char *line = NULL;
    size_t length = 0, count = 0;
    while (getline(&line, &length, file) != EOF)
    {
        ids[count] = malloc(strlen(line) + 1);
        strcpy(ids[count], line);
        ids[count][strlen(line) - 1] = 0;
        count++;
    }
    fclose(file);
    return (Input){
        ids,
        count};
}

void freeInput(Input input)
{
    int index = 0;
    while (input.length--)
        free(input.ids[index++]);
    free(input.ids);
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
    printf("P1: %d\n", results.part1);
    printf("P2: %s\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    freeInput(input);
    return 0;
}

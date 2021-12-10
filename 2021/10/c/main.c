#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct
{
    char **lines;
    int size, capacity;
} Input;
typedef struct
{
    int part1;
    unsigned long part2;
} Results;

typedef struct
{
    unsigned long *points;
    int size, capacity;
} IncompletePoints;

typedef struct
{
    char *closing;
    int size, capacity;
} Expected;

char getMatchingChar(char opening)
{
    switch (opening)
    {
        case '(': return ')';
        case '[': return ']';
        case '{': return '}';
        case '<': return '>';
    }
    perror("Unexpected opening character");
    exit(1);
}

int getIllegalPoints(char closing)
{
    switch (closing)
    {
        case ')': return 3;
        case ']': return 57;
        case '}': return 1197;
        case '>': return 25137;
    }
    printf("c: '%c': ", closing);
    perror("Unexpected illegal closing character");
    exit(1);
}

int getClosingPoints(char closing)
{
    switch (closing)
    {
        case ')': return 1;
        case ']': return 2;
        case '}': return 3;
        case '>': return 4;
    }
    perror("Unexpected closing character");
    exit(1);
}

#define INCOMPLETE_INCREMENT 10
void addToIncomplete(IncompletePoints *incomplete, unsigned long points)
{
    if (incomplete->size == incomplete->capacity)
        incomplete->points = realloc(incomplete->points, (incomplete->capacity += INCOMPLETE_INCREMENT) * sizeof(unsigned long));
    incomplete->points[incomplete->size++] = points;
}

#define EXPECTED_INCREMENT 5
void addToExpected(Expected *expected, char c)
{
    if (expected->size == expected->capacity)
        expected->closing = realloc(expected->closing, (expected->capacity += EXPECTED_INCREMENT) * sizeof(char));
    expected->closing[expected->size++] = c;
}

char getFromExpected(Expected *expected)
{
    if (!expected->size)
        return '\0';
    return expected->closing[--expected->size];
}

void swap(unsigned long *xp, unsigned long *yp)
{
    unsigned long temp = *xp;
    *xp = *yp;
    *yp = temp;
}

void bubbleSort(IncompletePoints incomplete)
{
    int i, j;
    for (i = 0; i < incomplete.size; i++)
        for (j = 0; j < incomplete.size - i - 1; j++)
            if (incomplete.points[j] > incomplete.points[j + 1])
                swap(&incomplete.points[j], &incomplete.points[j + 1]);
}

Results solve(Input input)
{
    int illegalPoints = 0;
    IncompletePoints incompletePoints = { 
        malloc(INCOMPLETE_INCREMENT * sizeof(unsigned long)),
        0, INCOMPLETE_INCREMENT
    };
    while (input.size--)
    {
        Expected expected = {
            malloc(EXPECTED_INCREMENT * sizeof(char)),
            0, EXPECTED_INCREMENT
        };
        int illegal = 0;
        char *line = *input.lines++, c;
        while ((c = *line++))
        {
            if (c == '(' || c == '[' || c == '{' || c == '<')
                addToExpected(&expected, getMatchingChar(c));
            else if (c != getFromExpected(&expected))
            {
                illegal = 1;
                illegalPoints += getIllegalPoints(c);
            }
        }
        if (!illegal)
        {
            unsigned long points = 0;
            while ((c = getFromExpected(&expected)))
                points = points * 5 + getClosingPoints(c);
            addToIncomplete(&incompletePoints, points);
        }
        free(expected.closing);
    }
    bubbleSort(incompletePoints);
    return (Results){illegalPoints, incompletePoints.points[incompletePoints.size / 2]};
}

#define INPUT_INCREMENTE 10
void addToInput(Input *input, const char *line)
{
    if (input->size == input->capacity)
    {
        input->capacity += INPUT_INCREMENTE;
        input->lines = realloc(input->lines, input->capacity * sizeof(char *));
    }
    input->lines[input->size] = malloc(strlen(line) + 1);
    strcpy(input->lines[input->size], line);
    input->size++;
}

char *rtrim(char *str, const char *seps)
{
    int i;
    if (seps == NULL)
        seps = "\t\n\v\f\r ";
    i = strlen(str) - 1;
    while (i >= 0 && strchr(seps, str[i]) != NULL)
        str[i--] = '\0';
    return str;
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
        malloc(INPUT_INCREMENTE * sizeof(char *)),
        0, INPUT_INCREMENTE
    };
    char *line = NULL;
    size_t len;
    while (getline(&line, &len, file) != EOF)
        addToInput(&input, rtrim(line, "\n"));
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    while (input.size--)
        free(*input.lines++);
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
    printf("P2: %lu\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <limits.h>

typedef struct {
    int count, capacity;
    char **messages;
} Input;
typedef struct
{
    char *part1;
    char *part2;
} Results;

int *getColumnRecords(Input input, int columnCount)
{
    int *columnRecords = calloc(columnCount, sizeof(int) * 26);
    int column;
    char *message, c;
    while (input.count--)
    {
        column = 0;
        message = *(input.messages++);
        while ((c = *(message++)) != 0)
            columnRecords[(c - 'a') * columnCount + column++]++;
    }
    return columnRecords;
}

char getMinForColumn(int *columnRecords, int column, int columnCount)
{
    int c, min = INT_MAX, letterCount;
    for (int letter = 0; letter < 26; letter++)
    {
        if ((letterCount = columnRecords[column + letter * columnCount]) < min)
        {
            min = letterCount;
            c = letter;
        }
    }
    return c + 'a';
}

char getMaxForColumn(int *columnRecords, int column, int columnCount)
{
    int c, max = 0, letterCount;
    for (int letter = 0; letter < 26; letter++)
    {
        if ((letterCount = columnRecords[column + letter * columnCount]) > max)
        {
            max = letterCount;
            c = letter;
        }
    }
    return c + 'a';
}

Results solve(Input input)
{
    int columnCount = strlen(input.messages[0]);
    int *columnRecords = getColumnRecords(input, columnCount);
    char *p1 = calloc(columnCount, 1), *p2 = calloc(columnCount + 1, 1);
    p1[columnCount] = p2[columnCount] = 0;
    for (int column = 0; column < columnCount; column++)
    {
        p1[column] = getMaxForColumn(columnRecords, column, columnCount);
        p2[column] = getMinForColumn(columnRecords, column, columnCount);
    }
    free(columnRecords);
    return (Results){p1, p2};
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

#define INPUT_INCREMENT 10
void addToInput(Input *input, char *message)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        char **oldMessages = input->messages;
        char **newMessages = realloc(oldMessages, input->capacity * sizeof(char*));
        input->messages = newMessages;
    }
    input->messages[input->count++] = message;
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
        0, INPUT_INCREMENT,
        calloc(INPUT_INCREMENT, sizeof(char*))
    };
    char *line, *message;
    size_t lineLength;
    while (getline(&line, &lineLength, file) != EOF)
    {
        message = malloc(strlen(line) + 1);
        strcpy(message, rtrim(line, NULL));
        addToInput(&input, message);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    char **messages = input.messages;
    while (input.count--)
        free(*(messages++));
    free(input.messages);
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
    printf("P1: %s\n", results.part1);
    printf("P2: %s\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}
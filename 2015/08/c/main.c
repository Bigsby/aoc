#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct {
    int count, capacity;
    char ** strings;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

char* replaceWord(const char* string, const char* oldWord, const char* newWord, int addedCount)
{
    char* result;
    int i, count = 0;
    int newWordlen = strlen(newWord);
    int oldWordlen = strlen(oldWord) + addedCount;
    for (i = 0; string[i] != '\0'; i++) {
        if (strstr(&string[i], oldWord) == &string[i]) {
            count++;
            i += oldWordlen - 1;
        }
    }
    result = (char*)malloc(i + count * (newWordlen - oldWordlen) + 1);
    i = 0;
    while (*string) {
        if (strstr(string, oldWord) == string) {
            strcpy(&result[i], newWord);
            i += newWordlen;
            string += oldWordlen;
        }
        else
            result[i++] = *string++;
    }
    result[i] = '\0';
    return result;
}

int part1(char *string)
{
    char *stripped = replaceWord(string, "\\\\", "r", 0);
    stripped = replaceWord(stripped, "\\\"", "r", 0);
    stripped = replaceWord(stripped, "\\x", "r", 2);
    return strlen(string) - strlen(stripped) + 2;
}

int part2(char *string)
{
    char *added = replaceWord(string, "\\", "\\\\", 0);
    added = replaceWord(added, "\"", "\\\"", 0);
    return 2 + strlen(added) - strlen(string);
}

int sumDifferences(Input input, int (*diffFunc)(char *))
{
    int total = 0;
    while (input.count--)
    {
        char string[strlen(*input.strings) + 1];
        strcpy(string, *input.strings);
        total += diffFunc(string);
        input.strings++;
    }
    return total;
}

Results solve(Input input)
{
    return (Results){sumDifferences(input, part1), sumDifferences(input, part2)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, char *string)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->strings = realloc(input->strings, input->capacity * sizeof(char *));
    }
    input->strings[input->count] = malloc(strlen(string) + 1);
    strcpy(input->strings[input->count], string);
    input->count++;
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
        malloc(sizeof(char*) * INPUT_INCREMENT) };
    char *line = NULL;
    size_t lineLength = 0, length;
    while (getline(&line, &lineLength, file) != EOF)
    {
        length = strlen(line);
        if (line[length - 1] == '\n')
            line[length-- - 1] = 0;
        addToInput(&input, line);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    char **strings = input.strings;
    while(input.count--)
        free(*(strings++));
    free(input.strings);
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

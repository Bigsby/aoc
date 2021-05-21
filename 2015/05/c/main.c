#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

typedef struct
{
    char **words;
    int count, size;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int countValidWords(Input input, int (*validationFunc)(char *))
{
    int total = 0;
    char *word;
    while (input.count--)
        total += validationFunc(*(input.words++));
    return total;
}

#define FORBINDEN_PAIRS_COUNT 4
const char *FORBIDEN_PAIRS[FORBINDEN_PAIRS_COUNT] = {"ab", "cd", "pq", "xy"};
int hasForbidenPairs(char *word)
{
    for (int index = 0; index < FORBINDEN_PAIRS_COUNT; index++)
        if (strstr(word, FORBIDEN_PAIRS[index]) != NULL)
            return 1;
    return 0;
}

int hasTwoOrMoreVowels(char *word)
{
    int count = 0;
    char c;
    while ((c = *word++) != '\0')
        switch (c)
        {
        case 'a':
        case 'e':
        case 'i':
        case 'o':
        case 'u':
            count++;
            break;
        }
    return count > 2;
}

int hasRepeatedLetters(char *word)
{
    int length = strlen(word);
    for (int index = 0; index < length - 1; index++)
        if (word[index] == word[index + 1])
            return 1;
    return 0;
}

int part1(char *word)
{
    return !hasForbidenPairs(word) && hasTwoOrMoreVowels(word) && hasRepeatedLetters(word);
}

int hasRepeatingPair(char *word)
{
    int length = strlen(word), index, offset;
    char pair[3];
    for (index = 0; index < length - 2; index++)
        if (strstr(word + index + 2, strncpy(pair, word + index, 2)) != NULL)
            return 1;
    return 0;
}

int hasRepeatingLetter(char *word)
{
    for (int index = 0; index < strlen(word) - 2; index++)
        if (word[index] == word[index + 2])
            return 1;
    return 0;
}

int part2(char *word)
{
    return hasRepeatingPair(word) && hasRepeatingLetter(word);
}

Results solve(Input input)
{
    return (Results){countValidWords(input, &part1), countValidWords(input, &part2)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, char *word)
{
    if (input->count == input->size)
    {
        char **oldWords = input->words;
        char **newWords = realloc(oldWords, (input->size + INPUT_INCREMENT) * sizeof(char *));
        input->words = newWords;
        input->size += INPUT_INCREMENT;
    }
    input->words[input->count] = malloc(strlen(word) + 1);
    strcpy(input->words[input->count], word);
    input->count++;
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
        calloc(10, sizeof(char *)),
        0,
        10};
    char *line = NULL;
    size_t lineLength;
    while (getline(&line, &lineLength, file) != EOF)
        addToInput(&input, rtrim(line, NULL));
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    char **words = input.words;
    while (input.count--)
        free (*(words++));
    free(input.words);
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
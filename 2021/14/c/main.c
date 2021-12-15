#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <math.h>

typedef struct {
    short *polymer;
    int polymerSize, polymerCapacity;
    short *pairs;
    short *insertions;
    int pairsSize, pairsCapacity;
    short *letters;
    int letterCount;
} Input;
typedef struct
{
    unsigned long part1;
    unsigned long part2;
} Results;

int getPairIndex(Input input, short pair)
{
    for (int index = 0; index < input.pairsSize; index++)
        if (input.pairs[index] == pair)
            return index;
    perror("Pair not found");
    exit(1);
}

int getLetterIndex(Input input, short letter)
{
    for (int letterIndex = 0; letterIndex < input.letterCount; letterIndex++)
        if (input.letters[letterIndex] == letter)
            return letterIndex;
    perror("Letter not found");
    exit(1);
}

unsigned long runInsertions(Input input, int steps)
{
    unsigned long *pairOccurences = calloc(input.pairsSize, sizeof(unsigned long));
    for (int index = 0; index < input.polymerSize - 1; index++)
        pairOccurences[getPairIndex(input, (input.polymer[index] << 8) + input.polymer[index + 1])]++;
    while (steps--)
    {
        unsigned long *newPairOccurences = calloc(input.pairsSize, sizeof(unsigned long));
        for (int pairIndex = 0; pairIndex < input.pairsSize; pairIndex++)
        {
            short pair = input.pairs[pairIndex];
            short first = pair >> 8;
            short second = pair & 0xFF;
            short newLetter = input.insertions[getPairIndex(input, pair)];
            unsigned long thisPairOccurences = pairOccurences[pairIndex];
            newPairOccurences[getPairIndex(input, (first << 8) | newLetter)] += thisPairOccurences;
            newPairOccurences[getPairIndex(input, (newLetter << 8) | second)] += thisPairOccurences;
        }
        free(pairOccurences);
        pairOccurences = newPairOccurences;
    }
    unsigned long *letterOccurences = calloc(input.letterCount, sizeof(unsigned long));
    for (int pairIndex = 0; pairIndex < input.pairsSize; pairIndex++)
        letterOccurences[getLetterIndex(input, input.pairs[pairIndex] & 0xFF)] += pairOccurences[pairIndex];
    letterOccurences[getLetterIndex(input, input.polymer[0])] += 1;
    unsigned long max = 0;
    unsigned long min = letterOccurences[0];
    for (int letterIndex = 0; letterIndex < input.letterCount; letterIndex++)
    {
        unsigned long occurences = letterOccurences[letterIndex];
        max = occurences > max ? occurences : max;
        min = occurences < min ? occurences : min;
    }
    free(letterOccurences);
    return max - min;
}

Results solve(Input input)
{
    return (Results){runInsertions(input, 10), runInsertions(input, 40)};
}

#define POLYMER_INCREMENT 5
#define PAIR_INCREMENT 10
void addToInputPolymer(Input *input, short letter)
{
    if (input->polymerSize == input->polymerCapacity)
        input->polymer = realloc(input->polymer, (input->polymerCapacity += POLYMER_INCREMENT) * sizeof(short));
    input->polymer[input->polymerSize++] = letter;
}

void addRuleToInput(Input *input, short pair, short insertion)
{
    if (input->pairsSize == input->pairsCapacity)
    {
        input->pairs = realloc(input->pairs, (input->pairsCapacity += PAIR_INCREMENT) * sizeof(short));
        input->insertions = realloc(input->insertions, input->pairsCapacity * sizeof(short));
    }
    input->pairs[input->pairsSize] = pair;
    input->insertions[input->pairsSize++] = insertion;
}

void setLetterIndex(Input *input, short letter)
{
    for (int letterIndex = 0; letterIndex < input->letterCount; letterIndex++)
        if (input->letters[letterIndex] == letter)
            return;
        else if (input->letters[letterIndex] == 0)
        {
            input->letters[letterIndex] = letter;
            return;
        }
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
        .polymer = malloc(POLYMER_INCREMENT * sizeof(short)),
        .polymerSize = 0,
        .polymerCapacity = POLYMER_INCREMENT,
        .pairs = malloc(PAIR_INCREMENT * sizeof(short)),
        .insertions = malloc(PAIR_INCREMENT * sizeof(short)),
        .pairsSize = 0,
        .pairsCapacity = PAIR_INCREMENT,
        .letters = NULL,
        .letterCount = 0
    };
    char *line = NULL;
    size_t len;
    getline(&line, &len, file);
    for (int index = 0; index < strlen(line) - 1; index++)
        addToInputPolymer(&input, line[index]);
    getline(&line, &len, file);
    while (getline(&line, &len, file) != EOF)
    {
        short pair = line[0] << 8;
        pair += line[1];
        addRuleToInput(&input, pair, line[6]);
    }
    input.letterCount = (int)sqrt(input.pairsSize);
    input.letters = calloc(input.letterCount, sizeof(short));
    for (int pairIndex = 0; pairIndex < input.pairsSize; pairIndex++)
    {
        short pair = input.pairs[pairIndex];
        short first = pair >> 8;
        short second = pair & 0xFF;
        setLetterIndex(&input, first);
        setLetterIndex(&input, second);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.polymer);
    free(input.pairs);
    free(input.insertions);
    free(input.letters);
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
    printf("P1: %lu\n", results.part1);
    printf("P2: %lu\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct
{
    char **passwords;
    int count;
    int size;
} Passphrase;

typedef struct
{
    Passphrase *passphrases;
    int count;
    int size;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int runTests(Input input, int (*validationFunc)(Passphrase))
{
    int valid = 0;
    while (input.count--)
        valid += validationFunc(*(input.passphrases++));
    return valid;
}

int noRepeatedPassords(Passphrase passphrase)
{
    int passwordCount = passphrase.count, occurences, passwordIndex;
    char **passwords = passphrase.passwords;
    while (passwordCount--)
    {
        occurences = 0;
        for (passwordIndex = 0; passwordIndex < passphrase.count; passwordIndex++)
            occurences += strcmp(*passwords, passphrase.passwords[passwordIndex]) == 0;
        if (occurences > 1)
            return 0;
        passwords++;
    }
    return 1;
}

void countLetterOccurrences(char *word, int *result)
{
    int index;
    for (index = 0; index < 26; index++)
        result[index] = 0;
    char c;
    while ((c = *(word++)))
        result[c - 'a']++;
}

int isAnagram(char *wordA, char *wordB)
{
    int aCounts[26], bCounts[26], index;
    countLetterOccurrences(wordA, aCounts);
    countLetterOccurrences(wordB, bCounts);
    for (index = 0; index < 26; index++)
        if (aCounts[index] != bCounts[index])
            return 0;
    return 1;
}

int noAnagrams(Passphrase passphrase)
{
    int thisIndex, otherIndex;
    for (thisIndex = 0; thisIndex < passphrase.count; thisIndex++)
        for (otherIndex = thisIndex + 1; otherIndex < passphrase.count; otherIndex++)
            if (isAnagram(passphrase.passwords[thisIndex], passphrase.passwords[otherIndex]))
                return 0;
    return 1;
}

Results solve(Input input)
{
    return (Results){runTests(input, &noRepeatedPassords), runTests(input, &noAnagrams)};
}

void addToPassphrase(Passphrase *passphrase, char *password)
{
    if (passphrase->count == passphrase->size)
    {
        char **oldPasswords = passphrase->passwords;
        char **newPasswords = realloc(oldPasswords, (passphrase->size + 2) * sizeof(char *));
        passphrase->passwords = newPasswords;
        passphrase->size += 2;
    }
    passphrase->passwords[passphrase->count] = malloc(strlen(password) + 1);
    strcpy(passphrase->passwords[passphrase->count], password);
    passphrase->count++;
}

void addToInput(Input *input, Passphrase passphrase)
{
    if (input->count == input->size)
    {
        Passphrase *oldPassphrases = input->passphrases;
        Passphrase *newPassphrases = realloc(oldPassphrases, (input->size + 10) * sizeof(Passphrase));
        input->passphrases = newPassphrases;
        input->size += 10;
    }
    input->passphrases[input->count++] = passphrase;
}

char *rtrim(char *str, const char *seps)
{
    int i;
    if (seps == NULL)
    {
        seps = "\t\n\v\f\r ";
    }
    i = strlen(str) - 1;
    while (i >= 0 && strchr(seps, str[i]) != NULL)
    {
        str[i] = '\0';
        i--;
    }
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
    size_t lineLength;
    char *line = NULL;
    Input input = {
        malloc(10 * sizeof(Passphrase)),
        0,
        10};
    while (getline(&line, &lineLength, file) != EOF)
    {
        Passphrase passphrase = {
            malloc(5 * sizeof(char *)),
            0,
            5};
        char *value = strtok(line, " ");
        while (value != NULL)
        {
            rtrim(value, NULL);
            addToPassphrase(&passphrase, value);
            value = strtok(NULL, " ");
        }
        addToInput(&input, passphrase);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    Passphrase *passphrases = input.passphrases;
    while (input.count--)
    {
        while (passphrases->count--)
        {
            free(*(passphrases->passwords));
            passphrases->passwords++;
        }
        passphrases++;
    }
    free(input.passphrases);
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
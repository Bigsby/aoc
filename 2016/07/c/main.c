#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

typedef struct
{
    int count, capacity;
    char **parts;
} IP;

typedef struct
{
    int count, capacity;
    IP *ips;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int hasABBA(char *part)
{
    int partLenth = strlen(part);
    for (int index = 0; index < partLenth - 3; index++)
        if (part[index] != part[index + 1] && part[index + 1] == part[index + 2] && part[index] == part[index + 3])
            return 1;
    return 0;
}

int supportsTLS(IP ip)
{
    int hypernets = 0, supernets = 0;
    for (int index = 0; index < ip.count; index++)
        if (index % 2)
            hypernets |= hasABBA(ip.parts[index]);
        else
            supernets |= hasABBA(ip.parts[index]);
    return !hypernets && supernets;
}

typedef struct
{
    char a, b;
} AB;

typedef struct
{
    int count, capacity;
    AB *abs;
} ABSet;

#define SET_INCREMENT 5

int setContains(ABSet set, char a, char b)
{
    AB ab;
    while (set.count--)
    {
        ab = *(set.abs++);
        if (ab.a == a && ab.b == b)
            return 1;
    }
    return 0;
}

void addToABSet(ABSet *set, char a, char b)
{
    if (setContains(*set, a, b))
        return;
    if (set->count == set->capacity)
    {
        set->capacity += SET_INCREMENT;
        AB *oldABs = set->abs;
        AB *newABs = realloc(oldABs, set->capacity * (sizeof(AB)));
        set->abs = newABs;
    }
    set->abs[set->count++] = (AB){a, b};
}

int supportsSSL(IP ip)
{
    ABSet abas = {
        0, SET_INCREMENT,
        malloc(SET_INCREMENT * sizeof(AB))};
    ABSet babs = {
        0, SET_INCREMENT,
        malloc(SET_INCREMENT * sizeof(AB))};
    int partLength, index;
    char *part;
    for (int partIndex = 0; partIndex < ip.count; partIndex++)
    {
        part = ip.parts[partIndex];
        partLength = strlen(part);
        for (index = 0; index < partLength - 2; index++)
            if (part[index] == part[index + 2] && part[index] != part[index + 1])
                if (partIndex % 2)
                    addToABSet(&abas, part[index], part[index + 1]);
                else
                    addToABSet(&babs, part[index + 1], part[index]);
    }
    AB ab;
    while (abas.count--)
    {
        ab = *(abas.abs++);
        if (setContains(babs, ab.a, ab.b))
            return 1;
    }
    return 0;
}

int countValidIps(Input input, int (*validationFunc)(IP))
{
    int count = 0;
    while (input.count--)
        count += validationFunc(*(input.ips++));
    return count;
}

Results solve(Input input)
{
    return (Results){countValidIps(input, &supportsTLS), countValidIps(input, &supportsSSL)};
}

#define INPUT_INCREMENT 10
#define IP_INCREMENT 2
void addToIp(IP *ip, char *part)
{
    if (ip->count == ip->capacity)
    {
        ip->capacity += IP_INCREMENT;
        char **oldParts = ip->parts;
        char **newParts = realloc(oldParts, ip->capacity * sizeof(char *));
        ip->parts = newParts;
    }
    int partLength = strlen(part);
    ip->parts[ip->count] = malloc(partLength + 1);
    if (ip->count % 2) // remove wrapping [ and ]
    {
        part[partLength - 1] = 0;
        part++;
    }
    strcpy(ip->parts[ip->count], part);
    ip->count++;
}

void addToInput(Input *input, IP ip)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        IP *oldIps = input->ips;
        IP *newIps = realloc(oldIps, input->capacity * sizeof(IP));
        input->ips = newIps;
    }
    input->ips[input->count++] = ip;
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    regex_t inputRegex;
#define INPUT_REGEX_GROUP_COUNT 3
    if (regcomp(&inputRegex, "(\\[?[a-z]+\\]?)", REG_EXTENDED))
    {
        perror("Error compiling hgt regex.");
        exit(1);
    }
    Input input = {
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(IP))};
    char *line = NULL, *cursor;
    size_t lineLength;
    regmatch_t groupArray[INPUT_REGEX_GROUP_COUNT];
    IP ip;
    int group;
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        ip = (IP){
            0, 3,
            malloc(3 * sizeof(char *))};
        while (!regexec(&inputRegex, cursor, INPUT_REGEX_GROUP_COUNT, groupArray, 0))
        {
            char cursorCopy[strlen(cursor) + 1];
            strcpy(cursorCopy, cursor);
            cursorCopy[groupArray[1].rm_eo] = 0;
            addToIp(&ip, cursorCopy + groupArray[1].rm_so);
            cursor += groupArray[0].rm_eo;
        }
        addToInput(&input, ip);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    IP *ips = input.ips, ip;
    while (input.count--)
    {
        ip = *(ips++);
        while (ip.count--)
            free(*(ip.parts++));
    }
    free(input.ips);
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
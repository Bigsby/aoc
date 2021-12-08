#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

const char *CENTER_OF_MASS = "COM";
const char *YOU = "YOU";
const char *SAN = "SAN";
#define INPUT_INCREMENT 10

typedef struct
{
    struct
    {
        int count, capacity;
        char **list;
    } planets;
    struct
    {
        int count, capacity;
        struct Orbit
        {
            int orbited, orbiter;
        } * list;
    } orbits;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int getPlanetIndex(Input *input, const char *planet)
{
    char **planets = input->planets.list;
    int index = 0;
    while (index < input->planets.count)
        if (strcmp(planet, input->planets.list[index++]) == 0)
            return index - 1;
    if (input->planets.count == input->planets.capacity)
    {
        input->planets.capacity += INPUT_INCREMENT;
        input->planets.list = realloc(input->planets.list, input->planets.capacity * sizeof(char *));
    }
    input->planets.list[input->planets.count] = malloc(4);
    strcpy(input->planets.list[input->planets.count], planet);
    return input->planets.count++;
}

#define NO_ORBITED -1
int getOrbitedPlanet(Input input, int orbiter)
{
    while (input.orbits.count--)
    {
        struct Orbit orbit = *(input.orbits.list++);
        if (orbit.orbiter == orbiter)
            return orbit.orbited;
    }
    return NO_ORBITED;
}

int allProcessed(int *processedOrbits, int count)
{
    while (count--)
        if (!*(processedOrbits++))
            return 0;
    return 1;
}

int part1(Input input)
{
    int planetsCount = input.planets.count;
    int *orbitCounts = calloc(planetsCount, sizeof(int));
    int *processedOrbits = calloc(planetsCount, sizeof(int));
    int centerOfMass = getPlanetIndex(&input, CENTER_OF_MASS);
    processedOrbits[centerOfMass] = 1;
    int index, orbited;
    while (!allProcessed(processedOrbits, planetsCount))
    {
        for (index = 0; index < planetsCount; index++)
        {
            if (processedOrbits[index])
                continue;
            if ((orbited = getOrbitedPlanet(input, index)) != NO_ORBITED)
            {
                if (processedOrbits[orbited])
                {
                    orbitCounts[index] = orbitCounts[orbited] + 1;
                    processedOrbits[index] = 1;
                }
            }
            else
            {
                orbitCounts[index] = 1;
                processedOrbits[index] = 1;
            }
        }
    }
    int totalOrbirCounts = 0;
    for (index = 0; index < planetsCount; index++)
        totalOrbirCounts += orbitCounts[index];
    free(orbitCounts);
    free(processedOrbits);
    return totalOrbirCounts;
}

typedef struct PathNode {
    int planet;
    struct PathNode *orbiter;
} PathNode;

PathNode *getPathToCenterOfMass(int planet, Input input)
{
    int centerOfMass = getPlanetIndex(&input, CENTER_OF_MASS);
    PathNode *previous = malloc(sizeof(PathNode));
    previous->planet = planet;
    previous->orbiter = NULL;
    PathNode *newNode;
    while ((planet = getOrbitedPlanet(input, planet)) != NO_ORBITED)
    {
        newNode = malloc(sizeof(PathNode));
        newNode->planet = planet;
        newNode->orbiter = previous;
        previous = newNode;
    }
    return previous;
}

int calculatePathLenth(PathNode *node)
{
    int length = 0;
    while ((node = node->orbiter) != NULL)
        length++;
    return length;
}

void freePath(PathNode *node)
{
    PathNode *currentNode = node;
    while (node != NULL)
    {
        currentNode = node->orbiter;
        free(node);
        node = currentNode;
    }
}

int part2(Input input)
{
    PathNode *youPath = getPathToCenterOfMass(getPlanetIndex(&input, YOU), input);
    PathNode *sanPath = getPathToCenterOfMass(getPlanetIndex(&input, SAN), input);
    PathNode *currentYou = youPath, *currentSan = sanPath;
    while (currentYou->planet == currentSan->planet)
    {
        currentYou = currentYou->orbiter;
        currentSan = currentSan->orbiter;
    }
    int result = calculatePathLenth(currentYou) + calculatePathLenth(currentSan);
    freePath(youPath);
    freePath(sanPath);
    return result;
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
}

void addOrbitToInput(Input *input, char *orbited, char *orbiter)
{
    int orbitedIndex = getPlanetIndex(input, orbited);
    int orbiterIndex = getPlanetIndex(input, orbiter);
    if (input->orbits.count == input->orbits.capacity)
    {
        input->orbits.capacity += INPUT_INCREMENT;
        struct Orbit *oldOrbits = input->orbits.list;
        struct Orbit *newOrbits = realloc(oldOrbits, input->orbits.capacity * sizeof(struct Orbit));
        input->orbits.list = newOrbits;
    }
    input->orbits.list[input->orbits.count++] = (struct Orbit){orbitedIndex, orbiterIndex};
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
#define INPUT_REGEX_GROUP_COUNT 4
    if (regcomp(&inputRegex, "^([A-Z0-9]{3})\\)([A-Z0-9]{3})", REG_EXTENDED))
    {
        perror("Error compiling hgt regex.");
        exit(1);
    }
    Input input = {
        {0, INPUT_INCREMENT,
         malloc(INPUT_INCREMENT * sizeof(char *))},
        {0, INPUT_INCREMENT,
         malloc(INPUT_INCREMENT * sizeof(struct Orbit))}};
    char *line = NULL, *cursor, orbited[4], orbiter[4];
    size_t lineLength;
    regmatch_t groupArray[INPUT_REGEX_GROUP_COUNT];
    int group;
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        if (!regexec(&inputRegex, cursor, INPUT_REGEX_GROUP_COUNT, groupArray, 0))
        {
            for (group = 0; group <= INPUT_REGEX_GROUP_COUNT && groupArray[group].rm_so != -1; group++)
            {
                char cursorCopy[strlen(cursor) + 1];
                strcpy(cursorCopy, cursor);
                cursorCopy[groupArray[group].rm_eo] = 0;
                switch (group)
                {
                case 1:
                    strcpy(orbited, cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    strcpy(orbiter, cursorCopy + groupArray[group].rm_so);
                    break;
                }
            }
            cursor += groupArray[0].rm_eo;
            addOrbitToInput(&input, orbited, orbiter);
        }
        else
        {
            perror("Bad format line");
            perror(line);
            exit(1);
        }
    }
    fclose(file);
    return input;
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

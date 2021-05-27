#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

typedef struct
{
    int weight, count, capacity;
    int *children;
} Record;

typedef struct
{
    int count, capacity;
    char **names;
    Record *records;
} Input;
typedef struct
{
    const char *part1;
    int part2;
} Results;

int getRecordIndex(Input *input, const char *name);

const char *part1(Input input)
{
    int *childrenLog = calloc(input.count, sizeof(int));
    int index;
    Record record;
    for (index = 0; index < input.count; index++)
    {
        record = input.records[index];
        if (record.count)
            while (record.count--)
                childrenLog[*(record.children++)] |= 1;
    }
    for (index = 0; index < input.count; index++)
    {
        if (!childrenLog[index])
            break;
    }
    free(childrenLog);
    return input.names[index];
}

int allNonZero(int *weights, int count)
{
    while (count--)
        if (*(weights++) == 0)
            return 0;
    return 1;
}

int part2(Input input, const char *topTower)
{
    int *combinedWeights = calloc(input.count, sizeof(int));
    int index, childIndex, allChildrenCombined, combinedWeight;
    int childWeight, firstWeight, secondWeight, firstWeightCount, secondWeightCount, firstWeightIndex, secondWeightIndex;
    Record record;
    while (!allNonZero(combinedWeights, input.count))
    {
        for (index = 0; index < input.count; index++)
        {
            if (combinedWeights[index])
                continue;
            record = input.records[index];
            if (!record.count)
            {
                combinedWeights[index] = record.weight;
                continue;
            }
            allChildrenCombined = 1;
            for (childIndex = 0; childIndex < record.count; childIndex++)
                if (!(allChildrenCombined &= combinedWeights[record.children[childIndex]] != 0))
                    break;
            if (allChildrenCombined)
            {
                combinedWeights[index] = record.weight;
                for (childIndex = 0; childIndex < record.count; childIndex++)
                    combinedWeights[index] += combinedWeights[record.children[childIndex]];
            }
        }
    }
    int currentTower = getRecordIndex(&input, topTower);
    int weightDifference = 0, multipleWeigths, weight;
    while (1)
    {
        firstWeight = secondWeight = 0;
        firstWeightCount = secondWeightCount = 0;
        record = input.records[currentTower];
        for (childIndex = 0; childIndex < record.count; childIndex++)
        {
            childWeight = combinedWeights[record.children[childIndex]];
            if (!firstWeight || firstWeight == childWeight)
            {
                firstWeight = childWeight;
                firstWeightCount++;
                firstWeightIndex = record.children[childIndex];
            }
            else
            {
                secondWeight = childWeight;
                secondWeightCount++;
                secondWeightIndex = record.children[childIndex];
            }
        }
        if (firstWeightCount && secondWeightCount)
        {
            currentTower = firstWeightCount == 1 ? firstWeightIndex : secondWeightIndex;
            weightDifference = firstWeight > secondWeightIndex ? firstWeight - secondWeight : secondWeight - firstWeight;
        }
        else
            return record.weight + weightDifference;
    }
}

Results solve(Input input)
{
    const char *part1Result = part1(input);
    return (Results){part1Result, part2(input, part1Result)};
}

#define INPUT_INCREMENT 10
int getRecordIndex(Input *input, const char *name)
{
    for (int index = 0; index < input->count; index++)
        if (strcmp(input->names[index], name) == 0)
            return index;
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        char **oldNames = input->names;
        char **newNames = realloc(oldNames, input->capacity * sizeof(char *));
        input->names = newNames;
        Record *oldRecords = input->records;
        Record *newRecords = realloc(oldRecords, input->capacity * sizeof(Record));
        input->records = newRecords;
    }
    input->names[input->count] = malloc(strlen(name) + 1);
    strcpy(input->names[input->count], name);
    input->count++;
    return input->count - 1;
}

void addToInput(Input *input, int recordIndex, Record record)
{
    input->records[recordIndex] = record;
}

#define RECORD_INCREMENT 2
void addToRecord(Record *record, Input *input, char *child)
{
    if (record->count == record->capacity)
    {
        record->capacity += RECORD_INCREMENT;
        int *oldChildren = record->children;
        int *newChildren = realloc(oldChildren, record->capacity * sizeof(int));
        record->children = newChildren;
    }
    record->children[record->count++] = getRecordIndex(input, child);
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
    regex_t inputRegex;
#define INPUT_REGEX_GROUP_COUNT 4
    if (regcomp(&inputRegex, "^([a-z]+) \\(([0-9]+)\\)(.*)", REG_EXTENDED))
    {
        perror("Error compiling input regex.");
        exit(1);
    }
    Input input = {
        0, 10,
        malloc(INPUT_INCREMENT * sizeof(char *)),
        malloc(INPUT_INCREMENT * sizeof(Record))};
    char *line = NULL, *cursor = NULL, *child;
    size_t lineLength;
    Record record;
    int group, recordIndex;
    regmatch_t groupArray[INPUT_REGEX_GROUP_COUNT];
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        record = (Record){
            0, 0, RECORD_INCREMENT,
            malloc(RECORD_INCREMENT * sizeof(int))};
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
                    recordIndex = getRecordIndex(&input, cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    record.weight = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 3:
                    cursor = cursorCopy + groupArray[group].rm_so;
                    if (cursor[1] == '-')
                    {
                        cursor += 4;
                        child = strtok(cursor, ", ");
                        while (child != NULL)
                        {
                            addToRecord(&record, &input, rtrim(child, NULL));
                            child = strtok(NULL, ", ");
                        }
                    }
                    break;
                }
            }
        }
        else
        {
            perror("Bad format line");
            perror(line);
            exit(1);
        }
        addToInput(&input, recordIndex, record);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    for (int index; index < input.count; index)
        free(input.names[index]);
    free(input.records);
    free(input.names);
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
    printf("P2: %d\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}
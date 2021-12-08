#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

typedef struct
{
    int color, count;
} Rule;
typedef struct
{
    int count, capacity;
    Rule *rules;
} RuleSet;

typedef struct
{
    int count, capacity;
    char **colors;
    RuleSet *ruleSets;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int getColorIndex(Input *input, const char *name);

void getRulesContaing(int color, Input input, int *containing)
{
    int index, innerIndex, innerColor;
    for (index = 0; index < input.count; index++)
    {
        for (innerIndex = 0; innerIndex < input.ruleSets[index].count; innerIndex++)
            if ((innerColor = input.ruleSets[index].rules[innerIndex].color) == color)
            {
                containing[index] |= 1;
                getRulesContaing(index, input, containing);
            }
    }
}

int part1(Input input, int requiredColor)
{
    int *containing = calloc(input.count, sizeof(int));
    getRulesContaing(requiredColor, input, containing);
    int total = 0;
    for (int index = 0; index < input.count; index++)
        total += containing[index] != 0;
    free(containing);
    return total;
}

int getQuantityForColor(int color, Input input)
{
    int total = 0;
    for (int index = 0; index < input.ruleSets[color].count; index++)
        total += input.ruleSets[color].rules[index].count * (1 + getQuantityForColor(input.ruleSets[color].rules[index].color, input));
    return total;
}

const char *REQUIRED_COLOR = "shiny gold";
Results solve(Input input)
{
    int requiredColor = getColorIndex(&input, REQUIRED_COLOR);
    return (Results){part1(input, requiredColor), getQuantityForColor(requiredColor, input)};
}

#define INPUT_INCREMENT 10
int getColorIndex(Input *input, const char *color)
{
    int index;
    for (index = 0; index < input->count; index++)
        if (strcmp(input->colors[index], color) == 0)
            return index;
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->colors = realloc(input->colors, input->capacity * sizeof(char *));
        input->ruleSets = realloc(input->ruleSets, input->capacity * sizeof(RuleSet));
    }
    input->colors[input->count] = malloc(strlen(color) + 1);
    strcpy(input->colors[input->count], color);
    return input->count++;
}
void addToInput(Input *input, int index, RuleSet ruleSet)
{
    input->ruleSets[index] = ruleSet;
}

void addToRuleSet(Input *input, RuleSet *ruleSet, int index, int count)
{
    if (ruleSet->count == ruleSet->capacity)
    {
        ruleSet->capacity += INPUT_INCREMENT;
        ruleSet->rules = realloc(ruleSet->rules, ruleSet->capacity * sizeof(Rule));
    }
    ruleSet->rules[ruleSet->count++] = (Rule){index, count};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    regex_t bagsRegex, innerBagsRegex;
#define BAGS_REGEX_GROUP_COUNT 4
    if (regcomp(&bagsRegex, "^(.*) bags contain (.*)\\.", REG_EXTENDED))
    {
        perror("Error compiling bags regex.");
        exit(1);
    }
#define INNER_BAGS_REGEX_GROUP_COUNT 4
    if (regcomp(&innerBagsRegex, " ?([0-9]+) (.*) bag", REG_EXTENDED))
    {
        perror("Error compiling inner bags regex.");
        exit(1);
    }
    Input input = {
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(char *)),
        malloc(INPUT_INCREMENT * sizeof(RuleSet))};
    char *line = NULL, *cursor, innerBags[128], *innerBag;
    size_t lineLength;
    regmatch_t groupArray[BAGS_REGEX_GROUP_COUNT];
    int colorIndex, innerColorIndex, count, group;
    RuleSet ruleSet;
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        ruleSet = (RuleSet){
            0, INPUT_INCREMENT,
            malloc(INPUT_INCREMENT * sizeof(Rule))};
        if (!regexec(&bagsRegex, cursor, BAGS_REGEX_GROUP_COUNT, groupArray, 0))
        {
            char cursorCopy[strlen(cursor) + 1];
            strcpy(cursorCopy, cursor);
            for (group = 0; group <= BAGS_REGEX_GROUP_COUNT && groupArray[group].rm_so != -1; group++)
            {
                cursorCopy[groupArray[group].rm_eo] = 0;
                switch (group)
                {
                case 1:
                    colorIndex = getColorIndex(&input, cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    strcpy(innerBags, cursorCopy + groupArray[group].rm_so);
                    break;
                }
            }
            if (strcmp(innerBags, "no other bags"))
            {
                innerBag = strtok(innerBags, ",");
                while (innerBag != NULL)
                {
                    cursor = innerBag;
                    if (!regexec(&innerBagsRegex, cursor, INNER_BAGS_REGEX_GROUP_COUNT, groupArray, 0))
                    {
                        char innerCursorCopy[strlen(cursor) + 1];
                        strcpy(innerCursorCopy, cursor);
                        for (group = 0; group <= INNER_BAGS_REGEX_GROUP_COUNT && groupArray[group].rm_so != -1; group++)
                        {
                            innerCursorCopy[groupArray[group].rm_eo] = 0;
                            switch (group)
                            {
                            case 1:
                                count = atoi(innerCursorCopy + groupArray[group].rm_so);
                                break;
                            case 2:
                                innerColorIndex = getColorIndex(&input, innerCursorCopy + groupArray[group].rm_so);
                                break;
                            }
                        }
                        addToRuleSet(&input, &ruleSet, innerColorIndex, count);
                    }
                    else
                    {
                        perror("Bad format inner bags");
                        perror(cursor);
                        exit(1);
                    }
                    innerBag = strtok(NULL, ",");
                }
            }
            addToInput(&input, colorIndex, ruleSet);
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
    for (int index = 0; index < input.count; index++)
    {
        free(input.colors[index]);
        free(input.ruleSets[index].rules);
    }
    free(input.colors);
    free(input.ruleSets);
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

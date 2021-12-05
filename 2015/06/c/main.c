#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

enum Actions
{
    ON,
    TOGGLE,
    OFF,
};
typedef struct
{
    int action, xStart, yStart, xEnd, yEnd;
} Instruction;

typedef struct
{
    int count, capacity;
    Instruction *instructions;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef int (*UpdateFunc)(int);

#define MATRIX_SIDE 1000
int runMatrix(Input input, UpdateFunc updateFuncs[3])
{
    int *matrix = calloc(MATRIX_SIDE * MATRIX_SIDE, sizeof(int));
    int x, y, position;
    while (input.count--)
    {
        int (*updateFunc)(int) = updateFuncs[input.instructions->action];
        for (x = input.instructions->xStart; x < input.instructions->xEnd + 1; x++)
            for (y = input.instructions->yStart; y < input.instructions->yEnd + 1; y++)
            {
                position = x + y * MATRIX_SIDE;
                matrix[position] = updateFunc(matrix[position]);
            }
        input.instructions++;
    }
    int total = 0;
    for (position = 0; position < MATRIX_SIDE * MATRIX_SIDE; position++)
        total += matrix[position];
    return total;
}

int p1TurnOn(int value)
{
    return 1;
}

int p1Toggle(int value)
{
    return !value;
}

int p1TurnOff(int value)
{
    return 0;
}

int p2TurnOn(int value)
{
    return value + 1;
}

int p2Toggle(int value)
{
    return value + 2;
}

int p2TurnOff(int value)
{
    return value > 0 ? value - 1 : 0;
}

Results solve(Input input)
{
    UpdateFunc p1Funcs[] = {
        p1TurnOn, p1Toggle, p1TurnOff};
    UpdateFunc p2Funcs[] = {
        p2TurnOn, p2Toggle, p2TurnOff};
    return (Results){
        runMatrix(input, p1Funcs),
        runMatrix(input, p2Funcs)};
}

#define ACTIONS_COUNT 3
const char *ACTIONS[ACTIONS_COUNT] = {
    "turn on",
    "toggle",
    "turn off"};

int getAction(char *action)
{
    for (int index = 0; index < ACTIONS_COUNT; index++)
        if (strcmp(action, ACTIONS[index]) == 0)
            return index;
    perror("Unknow action");
    perror(action);
    exit(1);
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, Instruction instruction)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->instructions = realloc(input->instructions, input->capacity * sizeof(Instruction));
    }
    input->instructions[input->count++] = instruction;
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
#define INPUT_REGEX_GROUP_COUNT 7
    regex_t inputRegex;
    if (regcomp(&inputRegex, "^(toggle|turn off|turn on) ([0-9]{1,3}),([0-9]{1,3}) through ([0-9]{1,3}),([0-9]{1,3})", REG_EXTENDED))
    {
        perror("Error compiling hgt regex.");
        exit(1);
    }
    Input input = {
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(Instruction))};
    char *line = NULL, *cursor = NULL;
    size_t lineLength;
    regmatch_t groupArray[INPUT_REGEX_GROUP_COUNT];
    int group, action, xStart, yStart, xEnd, yEnd;
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
                    action = getAction(cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    xStart = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 3:
                    yStart = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 4:
                    xEnd = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 5:
                    yEnd = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                }
            }
            cursor += groupArray[0].rm_eo;
            addToInput(&input, (Instruction){action, xStart, yStart, xEnd, yEnd});
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

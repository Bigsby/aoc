#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef enum {
    INCREMENT,
    DECREMENT
} Direction;
typedef enum {
    EQUAL,
    NOT_EQUAL,
    LESS_THAN,
    GREATER_THAN,
    LESS_OR_EQUAL,
    GREATER_OR_EQUAL
} Comparator;
typedef struct {
    int target, source, amount, value;
    Direction direction;
    Comparator comparator;
} Instruction;

typedef struct {
    int instructionCount, instructionCapacity;
    Instruction *instructions;
    int registerCount, registerCapacity;
    char **names;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int isConditionValid(int memoryValue, Comparator comparator, int value)
{
    switch (comparator)
    {
        case EQUAL:
            return memoryValue == value;
        case NOT_EQUAL:
            return memoryValue != value;
        case LESS_THAN:
            return memoryValue < value;
        case GREATER_THAN:
            return memoryValue > value;
        case LESS_OR_EQUAL:
            return memoryValue <= value;
        case GREATER_OR_EQUAL:
            return memoryValue >= value;
        default:
            perror("Unknow comparator to compare");
            exit(1);
    }
}

Results solve(Input input)
{
    int *memory = calloc(input.registerCount, sizeof(int));
    Instruction *instruction;
    int maxValue = 0;
    while (input.instructionCount--)
    {
        instruction = input.instructions++;
        if (isConditionValid(memory[instruction->source], instruction->comparator, instruction->value))
        {
            memory[instruction->target] += instruction->amount * (instruction->direction == INCREMENT ? 1 : -1);
            maxValue = memory[instruction->target] > maxValue ? memory[instruction->target] : maxValue;
        }
    }
    int currentMax = 0;
    for (int index = 0; index < input.registerCount; index++)
        currentMax = memory[index] > currentMax ? memory[index] : currentMax;
    free(memory);
    return (Results){currentMax, maxValue};
}

#define INPUT_INCREMENT 10

int getRegister(Input *input, const char *name)
{
    for (int index = 0; index < input->registerCount; index++)
        if (!strcmp(input->names[index], name))
            return index;
    if (input->registerCount == input->registerCapacity)
    {
        input->registerCapacity += INPUT_INCREMENT;
        char **oldNames = input->names;
        char **newNames = realloc(oldNames, input->registerCapacity * sizeof(char*));
        input->names = newNames;
    }
    input->names[input->registerCount] = malloc(strlen(name) + 1);
    strcpy(input->names[input->registerCount], name);
    return input->registerCount++;
}

Direction getDirection(const char *direction)
{
    if (!strcmp(direction, "inc"))
        return INCREMENT;
    if (!strcmp(direction, "dec"))
        return DECREMENT;
    perror("Unknow direction");
    perror(direction);
    exit(1);
}

Comparator getComparator(const char *comparator)
{
    if (!strcmp(comparator, "=="))
        return EQUAL;
    if (!strcmp(comparator, "!="))
        return NOT_EQUAL;
    if (!strcmp(comparator, "<"))
        return LESS_THAN;
    if (!strcmp(comparator, ">"))
        return GREATER_THAN;
    if (!strcmp(comparator, "<="))
        return LESS_OR_EQUAL;
    if (!strcmp(comparator, ">="))
        return GREATER_OR_EQUAL;
    perror("Unknown comparator");
    perror(comparator);
    exit(1);
}

void addToInput(Input *input, const char *target, const char *source, const char *comparator, const char *direction, int amount, int value)
{
    if (input->instructionCount == input->instructionCapacity)
    {
        input->instructionCapacity += INPUT_INCREMENT;
        Instruction *oldInstructions = input->instructions;
        Instruction *newInstructions = realloc(oldInstructions, input->instructionCapacity * sizeof(Instruction));
        input->instructions = newInstructions;
    }
    input->instructions[input->instructionCount] = (Instruction) {
        getRegister(input, target),
        getRegister(input, source),
        amount, value,
        getDirection(direction),
        getComparator(comparator)
    };
    input->instructionCount++;
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    char *line = NULL;
    size_t lineLength;
    char target[5], direction[5], source[5], comparator[5];
    int amount, value;
    Input input = {
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(Instruction)),
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(char*))
    };
    while (getline(&line, &lineLength, file) != EOF)
    {
        if (sscanf(line, "%[^ ] %[^ ] %d if %[^ ] %[^ ] %d", &target, &direction, &amount, &source, &comparator, &value) == 6)
            addToInput(&input, target, source, comparator, direction, amount, value);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    for (int index = 0; index < input.registerCount; index++)
        free(input.names[index]);
    free(input.names);
    free(input.instructions);
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

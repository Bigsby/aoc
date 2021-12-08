#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef enum {
    JMP,
    NOP,
    ACC
} InstructionType;

typedef struct {
    InstructionType type;
    int argument;
} Instruction;

typedef struct {
    int count, capacity;
    Instruction *instructions;
} Input;

typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct {
    int success, accumulator;
} BootResult;

void runInstruction(Instruction instruction, int *accumulator, int *instructionPointer)
{
    *(accumulator) += instruction.type == ACC ? instruction.argument : 0;
    *(instructionPointer) += instruction.type == JMP ? instruction.argument : 1;
}

BootResult runBoot(Input input)
{
    int accumulator = 0, instructionPointer = 0;
    int visited[input.count];
    for (int index = 0; index < input.count; index++)
        visited[index] = 0;
    while (1)
    {
        visited[instructionPointer] = 1;
        runInstruction(input.instructions[instructionPointer], &accumulator, &instructionPointer);
        if (instructionPointer == input.count)
            return (BootResult){1, accumulator};
        if (visited[instructionPointer])
            return (BootResult){0, accumulator};
    }
}

BootResult switchAndTest(int index, Input input)
{
    InstructionType previousType = input.instructions[index].type;
    input.instructions[index].type = previousType == JMP ? NOP : JMP;
    BootResult result = runBoot(input);
    input.instructions[index].type = previousType;
    return result;
}

int part2(Input input)
{
    for (int index = 0; index < input.count; index++)
    {
        if (input.instructions[index].type == ACC)
            continue;
        BootResult result = switchAndTest(index, input);
        if (result.success)
            return result.accumulator;
    }
    perror("Valid boot not found");
    exit(1);
}

Results solve(Input input)
{
    return (Results){runBoot(input).accumulator, part2(input)};
}

InstructionType getType(const char *mnemonic)
{
    if (!strcmp(mnemonic, "jmp"))
        return JMP;
    if (!strcmp(mnemonic, "nop"))
        return NOP;
    if (!strcmp(mnemonic, "acc"))
        return ACC;
    perror("Unknown mnemonic");
    printf(" %s", mnemonic);
    perror(mnemonic);
    exit(1);
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, char *mnemonic, int argument)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->instructions = realloc(input->instructions, input->capacity * sizeof(Instruction));
    }
    input->instructions[input->count++] = (Instruction){getType(mnemonic), argument};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    char *line = NULL, mnemonic[5], argument[5];
    size_t lineLength;
    Input input = {
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(Instruction))
    };
    while (getline(&line, &lineLength, file) != EOF)
        if (sscanf(line, "%[^ ] %[^ \n]", mnemonic, argument) == 2)
            addToInput(&input, mnemonic, atoi(argument));
    fclose(file);
    return input;
}

void freeInput(Input input)
{
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

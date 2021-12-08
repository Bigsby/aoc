#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct
{
    int *memory, size, capacity;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct
{
    int *memory;
    int pointer;
    int running;
    int input;
    int output;
} IntCodeComputer;

char errorMessage[64];

int getParameter(IntCodeComputer *computer, int offset, int mode)
{
    int value = computer->memory[computer->pointer + offset];
    switch (mode)
    {
    case 0: // POSITION
        return computer->memory[value];
    case 1: // IMMEDIATE
        return value;
    }
    sprintf(errorMessage, "Unrecognized parameter mode '%d'\n", mode);
    perror(errorMessage);
    exit(1);
}

int getAddress(IntCodeComputer *computer, int offset)
{
    return computer->memory[computer->pointer + offset];
}

void tick(IntCodeComputer *computer)
{
    if (!computer->running)
        return;
    int instruction = computer->memory[computer->pointer];
    int opcode = instruction % 100, p1Mode = (instruction / 100) % 10, p2Mode = (instruction / 1000) % 10;
    switch (opcode)
    {
    case 1: // ADD
        computer->memory[getAddress(computer, 3)] = getParameter(computer, 1, p1Mode) + getParameter(computer, 2, p2Mode);
        computer->pointer += 4;
        break;
    case 2: // MUL
        computer->memory[getAddress(computer, 3)] = getParameter(computer, 1, p1Mode) * getParameter(computer, 2, p2Mode);
        computer->pointer += 4;
        break;
    case 3: // INPUT
        computer->memory[getAddress(computer, 1)] = computer->input;
        computer->pointer += 2;
        break;
    case 4: // OUTPUT
        computer->output = getParameter(computer, 1, p1Mode);
        computer->pointer += 2;
        break;
    case 5: // JMP_TRUE
        if (getParameter(computer, 1, p1Mode))
            computer->pointer = getParameter(computer, 2, p2Mode);
        else
            computer->pointer += 3;
        break;
    case 6: // JMP_FALSE
        if (!getParameter(computer, 1, p1Mode))
            computer->pointer = getParameter(computer, 2, p2Mode);
        else
            computer->pointer += 3;
        break;
    case 7: // LESS_THAN
        computer->memory[getAddress(computer, 3)] = getParameter(computer, 1, p1Mode) < getParameter(computer, 2, p2Mode)
                                                        ? 1
                                                        : 0;
        computer->pointer += 4;
        break;
    case 8: // LESS_THAN
        computer->memory[getAddress(computer, 3)] = getParameter(computer, 1, p1Mode) == getParameter(computer, 2, p2Mode)
                                                        ? 1
                                                        : 0;
        computer->pointer += 4;
        break;
    case 99: // HALT
        computer->running = 0;
        break;
    default:
        sprintf(errorMessage, "Unknow instruction '%d' at '%d'\n", opcode, computer->pointer);
        perror(errorMessage);
        exit(1);
        break;
    }
}

IntCodeComputer newComputer(Input memory, int input)
{
    int *newMemory = malloc(memory.size * sizeof(int));
    memcpy(newMemory, memory.memory, memory.size * sizeof(int));
    return (IntCodeComputer){
        newMemory,
        0,
        1,
        input,
        0};
}

int run(IntCodeComputer *computer)
{
    while (computer->running)
        tick(computer);
    free(computer->memory);
    return computer->output;
}

int runProgram(Input memory, int input)
{
    IntCodeComputer computer = newComputer(memory, input);
    return run(&computer);
}

Results solve(Input input)
{
    return (Results){runProgram(input, 1), runProgram(input, 5)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int value)
{
    if (input->size == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->memory = realloc(input->memory, input->capacity * sizeof(int));
    }
    input->memory[input->size++] = value;
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    rewind(file);
    char *content = malloc(length);
    fread(content, 1, length, file);
    Input input = {
        calloc(INPUT_INCREMENT, sizeof(int)),
        0,
        INPUT_INCREMENT};
    char *value = strtok(content, ",");
    while (value != NULL)
    {
        addToInput(&input, atoi(value));
        value = strtok(NULL, ",");
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.memory);
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

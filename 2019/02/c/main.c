#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct
{
    int *memory;
    size_t length;
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
} IntCodeComputer;

int getParameter(IntCodeComputer *computer, int offset)
{
    return computer->memory[computer->memory[computer->pointer + offset]];
}

int getAddress(IntCodeComputer *computer, int offset)
{
    return computer->memory[computer->pointer + offset];
}

char errorMessage[64];
void tick(IntCodeComputer *computer)
{
    if (!computer->running)
        return;
    int opcode = computer->memory[computer->pointer];
    switch (opcode)
    {
    case 1: // ADD
        computer->memory[getAddress(computer, 3)] = getParameter(computer, 1) + getParameter(computer, 2);
        computer->pointer += 4;
        break;
    case 2: // MUL
        computer->memory[getAddress(computer, 3)] = getParameter(computer, 1) * getParameter(computer, 2);
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

IntCodeComputer newComputer(Input input)
{
    int *newMemory = calloc(input.length, sizeof(int));
    int *address = newMemory;
    while (input.length--)
        *(address++) = *(input.memory++);
    return (IntCodeComputer){
        newMemory,
        0,
        1};
}

int run(IntCodeComputer *computer)
{
    while (computer->running)
        tick(computer);
    return computer->memory[0];
}

int runProgram(Input input, int noun, int verb)
{
    IntCodeComputer computer = newComputer(input);
    computer.memory[1] = noun;
    computer.memory[2] = verb;
    return run(&computer);
}

const int TARGET_VALUE = 19690720;

int part2(Input input)
{
    int noun, verb;
    for (noun = 0; noun < 100; noun++)
        for (verb = 0; verb < 100; verb++)
            if (runProgram(input, noun, verb) == TARGET_VALUE)
                return 100 * noun + verb;
    perror("Target value not found");
    exit(1);
}

Results solve(Input input)
{
    return (Results){runProgram(input, 12, 2), part2(input)};
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
    int *memory = calloc(512, sizeof(int));
    int count = 0;
    char *value = strtok(content, ",");
    while (value != NULL)
    {
        memory[count++] = atoi(value);
        value = strtok(NULL, ",");
    }
    fclose(file);
    return (Input){memory, count};
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
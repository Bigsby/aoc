#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <complex.h>
#include <string.h>

typedef double complex Lattice;

typedef struct {
    Lattice direction;
    int units;
} Command;

typedef struct {
    Command *commands;
    int count, capacity;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int part1(Input input)
{
    Lattice position = 0;
    while (input.count--)
    {
        position += input.commands->direction * input.commands->units;
        input.commands++;
    }
    return (int)(creal(position) * cimag(position));
}

int part2(Input input)
{
    Lattice position = 0;
    Lattice aim = 0;
    while (input.count--)
    {
        if (input.commands->direction == 1)
            position += input.commands->units * (1 + aim);
        else
            aim += input.commands->direction * input.commands->units;
        input.commands++;
    }
    return (int)(creal(position) * cimag(position));
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, Lattice direction, int units)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->commands = realloc(input->commands, input->capacity * sizeof(Command));
    }
    input->commands[input->count++] = (Command){
        direction,
        units
    };
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    size_t len = 0;
    char *line;
    char command[10];
    int units;
    Lattice direction;
    Input input = {
        malloc(INPUT_INCREMENT * sizeof(Command)),
        0, INPUT_INCREMENT
    };
    while (getline(&line, &len, file) != EOF)
    {
        sscanf(line, "%s %d", command, &units);
        if (strcmp(command, "forward") == 0)
            direction = 1;
        else if (strcmp(command, "down") == 0)
            direction = I;
        else if (strcmp(command, "up") == 0)
            direction = -I;
        else {
            perror("Unknow command");
            exit(1);
        }
        addToInput(&input, direction, units);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.commands);
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

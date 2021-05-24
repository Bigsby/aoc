#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

#define INPUT_INCREMENT 10

typedef enum
{
    SCALAR,
    WIRE
} OperandType;

typedef enum
{
    AND,
    OR,
    LSHIFT,
    RSHIFT
} OperationType;

typedef enum
{
    INPUT,
    NOT,
    BINARY
} ConnectionType;

typedef struct
{
    OperandType type;
    int value;
} Operand;

typedef struct
{
    ConnectionType type;
    Operand operand1, operand2;
    OperationType operation;
} Connection;

typedef struct
{
    int count, capacity;
    char **wires;
    Connection *connections;
} Input;

typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct
{
    int count;
    char **wires;
    Connection *connections;
    int *value;
    int *valuesFound;
} Circuit;

int getWireIndex(Input *input, const char *wire);
int getValueFromConnection(Circuit circuit, int target);

int getValueFromOperand(Circuit circuit, Operand operand)
{
    switch (operand.type)
    {
    case SCALAR:
        return operand.value;
    case WIRE:
        return getValueFromConnection(circuit, operand.value);
    default:
        perror("Unrecognized operand type");
        exit(1);
    }
}

int getValueFromBinaryConnection(Circuit circuit, Connection connection)
{
    int operand1 = getValueFromOperand(circuit, connection.operand1);
    int operand2 = getValueFromOperand(circuit, connection.operand2);
    switch (connection.operation)
    {
    case AND:
        return operand1 & operand2;
    case OR:
        return operand1 | operand2;
    case LSHIFT:
        return operand1 << operand2;
    case RSHIFT:
        return operand1 >> operand2;
    default:
        perror("Unrecognized binary operation");
        exit(1);
    }
}

int calculateValueForConnection(Circuit circuit, Connection connection)
{
    switch (connection.type)
    {
    case INPUT:
        return getValueFromOperand(circuit, connection.operand1);
    case NOT:
        return ~getValueFromOperand(circuit, connection.operand1);
    case BINARY:
        return getValueFromBinaryConnection(circuit, connection);
    default:
        perror("Unrecognized connection type");
        exit(1);
    }
}

int setValueOnCircuit(Circuit circuit, int target, int value)
{
    circuit.valuesFound[target] = 1;
    return circuit.value[target] = value;
}

int getValueFromConnection(Circuit circuit, int target)
{
    if (circuit.valuesFound[target])
        return circuit.value[target];
    return setValueOnCircuit(circuit, target, calculateValueForConnection(circuit, circuit.connections[target]));
}

Circuit createCircuit(Input input)
{
    return (Circuit){
        input.count,
        input.wires,
        input.connections,
        calloc(input.count, sizeof(int)),
        calloc(input.count, sizeof(int))};
}

void freeCircuit(Circuit circuit)
{
    free(circuit.value);
    free(circuit.valuesFound);
}

Results solve(Input input)
{
    Circuit circuit = createCircuit(input);
    int targetWire = getWireIndex(&input, "a");
    int part1Result = getValueFromConnection(circuit, targetWire);
    freeCircuit(circuit);
    circuit = createCircuit(input);
    setValueOnCircuit(circuit, getWireIndex(&input, "b"), part1Result);
    int part2Result = getValueFromConnection(circuit, targetWire);
    freeCircuit(circuit);
    return (Results){part1Result, part2Result};
}

int getWireIndex(Input *input, const char *wire)
{
    int index = 0;
    while (index < input->count)
        if (strcmp(wire, input->wires[index++]) == 0)
            return index - 1;
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        char **oldWires = input->wires;
        char **newWires = realloc(oldWires, input->capacity * sizeof(char *));
        input->wires = newWires;
        Connection *oldConnections = input->connections;
        Connection *newConnections = realloc(oldConnections, input->capacity * sizeof(Connection));
        input->connections = newConnections;
    }
    input->wires[input->count] = malloc(strlen(wire) + 1);
    strcpy(input->wires[input->count], wire);
    input->count++;
    return input->count - 1;
}

void addToInput(Input *input, const char *target, Connection connection)
{
    int wire = getWireIndex(input, target);
    input->connections[wire] = connection;
}

Operand getOperand(Input *input, const char *value)
{
    int scalar;
    if (sscanf(value, "%d", &scalar))
        return (Operand){SCALAR, scalar};
    return (Operand){WIRE, getWireIndex(input, value)};
}

OperationType getOperation(const char *value)
{
    if (strcmp(value, "AND") == 0)
        return AND;
    if (strcmp(value, "OR") == 0)
        return OR;
    if (strcmp(value, "LSHIFT") == 0)
        return LSHIFT;
    if (strcmp(value, "RSHIFT") == 0)
        return RSHIFT;
    perror("Unknow operation");
    perror(value);
    exit(1);
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    regex_t sourceTargetRegex, inputRegex, unaryRegex, binaryRegex;
    if (regcomp(&sourceTargetRegex, "^(.*) -> ([a-z]+)", REG_EXTENDED))
    {
        perror("Error compiling sourceTarget regex.");
        exit(1);
    }
    if (regcomp(&inputRegex, "^[^ ]+$", REG_EXTENDED))
    {
        perror("Error compiling input regex.");
        exit(1);
    }
    if (regcomp(&unaryRegex, "^NOT ([a-z]+)", REG_EXTENDED))
    {
        perror("Error compiling not regex.");
        exit(1);
    }
    if (regcomp(&binaryRegex, "^([a-z]+|[0-9]+) +(AND|OR|LSHIFT|RSHIFT) +([a-z]+|[0-9]+)", REG_EXTENDED))
    {
        perror("Error compiling not regex.");
        exit(1);
    }
    Input input = {
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(char *)),
        malloc(INPUT_INCREMENT * sizeof(Connection))};
#define REGEX_GROUP_COUNT 7
    char *line, *cursor, source[16], target[8];
    size_t lineLength;
    regmatch_t groupArray[REGEX_GROUP_COUNT];
    Operand operand1, operand2;
    OperationType operation;
    int group;
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        if (!regexec(&sourceTargetRegex, cursor, REGEX_GROUP_COUNT, groupArray, 0))
        {
            char cursorCopy[strlen(cursor) + 1];
            strcpy(cursorCopy, cursor);
            for (group = 0; group <= REGEX_GROUP_COUNT && groupArray[group].rm_so != -1; group++)
            {
                cursorCopy[groupArray[group].rm_eo] = 0;
                switch (group)
                {
                case 1:
                    strcpy(source, cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    strcpy(target, cursorCopy + groupArray[group].rm_so);
                    break;
                }
            }
            cursor = source;
            strcpy(cursorCopy, cursor);
            if (!regexec(&inputRegex, cursor, REGEX_GROUP_COUNT, groupArray, 0))
                addToInput(&input, target, (Connection){INPUT, getOperand(&input, source)});
            else if (!regexec(&unaryRegex, cursor, REGEX_GROUP_COUNT, groupArray, 0))
            {
                for (group = 0; group <= REGEX_GROUP_COUNT && groupArray[group].rm_so != -1; group++)
                {
                    cursorCopy[groupArray[group].rm_eo] = 0;
                    switch (group)
                    {
                    case 1:
                        operand1 = getOperand(&input, cursorCopy + groupArray[group].rm_so);
                        break;
                    }
                }
                addToInput(&input, target, (Connection){NOT, operand1});
            }
            else if (!regexec(&binaryRegex, cursor, REGEX_GROUP_COUNT, groupArray, 0))
            {
                for (group = 0; group <= REGEX_GROUP_COUNT && groupArray[group].rm_so != -1; group++)
                {
                    cursorCopy[groupArray[group].rm_eo] = 0;
                    switch (group)
                    {
                    case 1:
                        operand1 = getOperand(&input, cursorCopy + groupArray[group].rm_so);
                        break;
                    case 2:
                        operation = getOperation(cursorCopy + groupArray[group].rm_so);
                        break;
                    case 3:
                        operand2 = getOperand(&input, cursorCopy + groupArray[group].rm_so);
                        break;
                    }
                }
                addToInput(
                    &input,
                    target,
                    (Connection){BINARY, operand1, operand2, operation});
            }
            else
            {
                perror("Unknow connection source");
                perror(source);
                exit(1);
            }
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
    int index = 0;
    while (index < input.count)
        free(input.wires[index++]);
    free(input.wires);
    free(input.connections);
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
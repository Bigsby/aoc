#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct
{
    long *memory, size, capacity;
} Input;
typedef struct
{
    long part1;
    long part2;
} Results;

#pragma region Queue
typedef struct QueueNode
{
    long value;
    struct QueueNode *next;

} QueueNode;

QueueNode *enqueue(QueueNode *head, long value)
{
    if (head == NULL)
    {
        QueueNode *node = malloc(sizeof(QueueNode));
        node->value = value;
        node->next = NULL;
        head = node;
    }
    else
        head->next = enqueue(head->next, value);
    return head;
}

int isQueueEmpty(QueueNode *head)
{
    return head == NULL;
}

QueueNode *dequeue(QueueNode *head, long *value)
{
    if (head == NULL)
    {
        perror("dequeing from empty queue");
        exit(1);
    }
    else
    {
        *(value) = head->value;
        QueueNode *next = head->next;
        free(head);
        return next;
    }
}

void freeQueue(QueueNode *node)
{
    if (node != NULL)
    {
        freeQueue(node->next);
        free(node);
    }
}
#pragma endregion

#pragma region Memory
typedef struct {
    long *memory;
    long size;
    long *outliers;
    long *outliersAddresses;
    int outliersSize;
    int outliersCapacity;
} Memory;

#define OUTLIERS_INCREMENT 5


Memory newMemory(Input input)
{
    Memory newMemory = {
        .memory = malloc(input.size * sizeof(long)),
        .size = input.size,
        .outliers = malloc(OUTLIERS_INCREMENT * sizeof(long)),
        .outliersAddresses = malloc(OUTLIERS_INCREMENT * sizeof(long)),
        .outliersSize = 0,
        .outliersCapacity = OUTLIERS_INCREMENT
    };
    memcpy(newMemory.memory, input.memory, input.size * sizeof(long));
    return newMemory;
}

void freeMemory(Memory memory)
{
    free(memory.memory);
    free(memory.outliers);
    free(memory.outliersAddresses);
}

long *addToOutliers(Memory *memory, long address)
{
    if (memory->outliersSize == memory->outliersCapacity)
    {
        memory->outliersCapacity += OUTLIERS_INCREMENT;
        memory->outliers = realloc(memory->outliers, memory->outliersCapacity * sizeof(long));
        memory->outliersAddresses = realloc(memory->outliersAddresses, memory->outliersCapacity * sizeof(long));
    }
    memory->outliersAddresses[memory->outliersSize] = address;
    long *pointer = memory->outliers + memory->outliersSize++;
    *pointer = 0;
    return pointer;
}

long *getMemoryPointer(Memory *memory, long address)
{
    if (address < memory->size)
        return memory->memory + address;
    for (long index = 0; index < memory->outliersSize; index++)
        if (memory->outliersAddresses[index] == address)
            return memory->outliers + index;
    return addToOutliers(memory, address);
}

void setMemoryValue(Memory *memory, long address, long value)
{
    *(getMemoryPointer(memory, address)) = value;
}

long getMemoryValue(Memory *memory, long address)
{
    return *(getMemoryPointer(memory, address));
}
#pragma endregion

#pragma region IntCodeComputer
typedef struct
{
    Memory memory;
    long pointer;
    unsigned long base;
    int running;
    QueueNode *input;
    QueueNode *output;
} IntCodeComputer;

IntCodeComputer newComputer(Input memory)
{
    return (IntCodeComputer){
        newMemory(memory),
        0,
        0,
        1,
        NULL,
        NULL};
}

char errorMessage[64];

long getParameter(IntCodeComputer *computer, int offset, int mode)
{
    long value = getMemoryValue(&(computer->memory), computer->pointer + offset);
    switch (mode)
    {
        case 0: // POSITION
            return getMemoryValue(&(computer->memory), value);
        case 1: // IMMEDIATE
            return value;
        case 2: // RELATIVE
            return getMemoryValue(&(computer->memory), computer->base + value);
    }
    sprintf(errorMessage, "Unrecognized parameter mode '%d'\n", mode);
    perror(errorMessage);
    exit(1);
}

void setAddressValue(IntCodeComputer *computer, int offset, int mode, long value)
{
    long address = getMemoryValue(&(computer->memory), computer->pointer + offset);
    switch (mode)
    {
        case 0: // POSITIION
            setMemoryValue(&(computer->memory), address, value);
            break;
        case 2: // RELATIVE
            setMemoryValue(&(computer->memory), computer->base + address, value);
            break;
        default:
            sprintf(errorMessage, "Unrecognized address mode '%d'\n", mode);
            perror(errorMessage);
            exit(1);
    }
}

int tick(IntCodeComputer *computer)
{
    if (!computer->running)
        return 0;
    int instruction = getMemoryValue(&computer->memory, computer->pointer);
    int opcode = instruction % 100, p1Mode = (instruction / 100) % 10, p2Mode = (instruction / 1000) % 10, p3Mode = (instruction / 10000) % 10;
    switch (opcode)
    {
    case 1: // ADD
        setAddressValue(computer, 3, p3Mode, getParameter(computer, 1, p1Mode) + getParameter(computer, 2, p2Mode));
        computer->pointer += 4;
        break;
    case 2: // MUL
        setAddressValue(computer, 3, p3Mode, getParameter(computer, 1, p1Mode) * getParameter(computer, 2, p2Mode));
        computer->pointer += 4;
        break;
    case 3: // INPUT
        if (!isQueueEmpty(computer->input))
        {
            long value;
            computer->input = dequeue(computer->input, &value);
            setAddressValue(computer, 1, p1Mode, value);
            computer->pointer += 2;
        }
        break;
    case 4: // OUTPUT
        computer->output = enqueue(computer->output, getParameter(computer, 1, p1Mode));
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
        setAddressValue(computer, 3, p3Mode, getParameter(computer, 1, p1Mode) < getParameter(computer, 2, p2Mode)
                                                        ? 1
                                                        : 0);
        computer->pointer += 4;
        break;
    case 8: // LESS_THAN
        setAddressValue(computer, 3, p3Mode, getParameter(computer, 1, p1Mode) == getParameter(computer, 2, p2Mode)
                                                        ? 1
                                                        : 0);
        computer->pointer += 4;
        break;
    case 9:
        computer->base += getParameter(computer, 1, p1Mode);
        computer->pointer += 2;
        break;
    case 99: // HALT
        computer->running = 0;
        break;
    default:
        sprintf(errorMessage, "Unknow instruction '%d' at '%ld'\n", opcode, computer->pointer);
        perror(errorMessage);
        exit(1);
        break;
    }
    return computer->running;
}

void addToComputerInput(IntCodeComputer *computer, int value)
{
    computer->input = enqueue(computer->input, value);
}

void freeComputer(IntCodeComputer *computer)
{
    freeMemory(computer->memory);
    freeQueue(computer->input);
}
#pragma endregion

long run(Input input, long mode)
{
    IntCodeComputer computer = newComputer(input);
    addToComputerInput(&computer, mode);
    while (tick(&computer))
        ;
    long result;
    dequeue(computer.output, &result);
    freeComputer(&computer);
    return result;
}

Results solve(Input input)
{
    return (Results) {
        run(input, 1),
        run(input, 2)
    };
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, long value)
{
    if (input->size == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->memory = realloc(input->memory, input->capacity * sizeof(long));
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
        calloc(INPUT_INCREMENT, sizeof(long)),
        0,
        INPUT_INCREMENT};
    char *value = strtok(content, ",");
    while (value != NULL)
    {
        addToInput(&input, atol(value));
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
    printf("P1: %ld\n", results.part1);
    printf("P2: %ld\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}

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

#pragma region Queue
typedef struct QueueNode
{
    int value;
    struct QueueNode *next;

} QueueNode;

QueueNode *enqueue(QueueNode *head, int value)
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

QueueNode *dequeue(QueueNode *head, int *value)
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

#pragma region IntCodeComputer
typedef struct
{
    int *memory;
    int pointer;
    int running;
    QueueNode *input;
    QueueNode *output;
} IntCodeComputer;

IntCodeComputer newComputer(Input memory)
{
    int *newMemory = malloc(memory.size * sizeof(int));
    memcpy(newMemory, memory.memory, memory.size * sizeof(int));
    return (IntCodeComputer){
        newMemory,
        0,
        1,
        NULL,
        NULL};
}

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

int tick(IntCodeComputer *computer)
{
    if (!computer->running)
        return 0;
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
        if (!isQueueEmpty(computer->input))
        {
            int value;
            computer->input = dequeue(computer->input, &(computer->memory[getAddress(computer, 1)]));
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
    return computer->running;
}

void addToComputerInput(IntCodeComputer *computer, int value)
{
    computer->input = enqueue(computer->input, value);
}

void freeComputer(IntCodeComputer *computer)
{
    free(computer->memory);
    freeQueue(computer->input);
}
#pragma endregion

int run(IntCodeComputer *computer)
{
    while (tick(computer))
        ;
    int result;
    dequeue(computer->output, &result);
    freeComputer(computer);
    return result;
}

int next_permutation(int *indexes, int count)
{
#define swap(i, j)               \
    {                            \
        t = indexes[i];          \
        indexes[i] = indexes[j]; \
        indexes[j] = t;          \
    }
    int k, l, t;
    for (k = count - 1; k && indexes[k - 1] >= indexes[k]; k--)
        ;
    if (!k--)
        return 0;
    for (l = count - 1; indexes[l] <= indexes[k]; l--)
        ;
    swap(k, l);
    for (k++, l = count - 1; l > k; l--, k++)
        swap(k, l);
    return 1;
#undef swap
}

int runPhasesPermutation(Input input, int *phases)
{
    int output = 0;
    for (int phaseIndex = 0; phaseIndex < 5; phaseIndex++)
    {
        IntCodeComputer computer = newComputer(input);
        addToComputerInput(&computer, phases[phaseIndex]);
        addToComputerInput(&computer, output);
        output = run(&computer);
    }
    return output;
}

int getMaxFromPermutations(Input input, int (*runningFunc)(Input, int *))
{
    int phases[5], phaseIndex;
    for (phaseIndex = 0; phaseIndex < 5; phaseIndex++)
        phases[phaseIndex] = phaseIndex;
    int max = 0, result;
    do
    {
        max = (result = runningFunc(input, phases)) > max ? result : max;
    } while (next_permutation(phases, 5));
    return max;
}

int anyRunning(IntCodeComputer *amplifiers, int count)
{
    while (count--)
        if ((amplifiers++)->running)
            return 1;
    return 0;
}

int runFeedbackPhasesPermutation(Input input, int *phases)
{
    IntCodeComputer amplifiers[5];
    int phaseIndex, output, lastOutput;
    for (phaseIndex = 0; phaseIndex < 5; phaseIndex++)
    {
        amplifiers[phaseIndex] = newComputer(input);
        addToComputerInput(&amplifiers[phaseIndex], phases[phaseIndex] + 5);
    }
    addToComputerInput(&amplifiers[0], 0);
    while (anyRunning(amplifiers, 5))
    {
        for (phaseIndex = 0; phaseIndex < 5; phaseIndex++)
        {
            tick(&(amplifiers[phaseIndex]));
            if (!isQueueEmpty(amplifiers[phaseIndex].output))
            {
                amplifiers[phaseIndex].output = dequeue(amplifiers[phaseIndex].output, &output);
                if (phaseIndex == 4)
                    lastOutput = output;
                addToComputerInput(&amplifiers[(phaseIndex + 1) % 5], output);
            }
        }
    }
    for (phaseIndex = 0; phaseIndex < 5; phaseIndex++)
        freeComputer(&(amplifiers[phaseIndex]));
    return lastOutput;
}

Results solve(Input input)
{
    return (Results){
        getMaxFromPermutations(input, runPhasesPermutation),
        getMaxFromPermutations(input, runFeedbackPhasesPermutation)};
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

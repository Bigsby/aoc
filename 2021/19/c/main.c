#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>

typedef int Beacon[3];
typedef struct {
    Beacon *beacons;
    int size, capacity;
} BeaconList;
typedef struct { 
    BeaconList *scanners;
    int size, capacity;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct {
    int *indexes, current;
} IndexQueue;

typedef struct {
    int *differences, *counts, size;
} Counter;

#define LIST_INCREMENT 10
#define EMPTY_QUEUE -1

int nextInQueue(int *queue, int size)
{
    for (int index = 0; index < size; index++)
        if (queue[index])
            return index;
    return EMPTY_QUEUE;
}

int addToCounter(Counter *counter, int difference)
{
    for (int index = 0; index < counter->size; index++)
        if (counter->differences[index] == difference)
            return (++counter->counts[index]);
    counter->differences[counter->size] = difference;
    counter->counts[counter->size++] = 1;
    return 1;
}

void addToListUnique(BeaconList *scanner, int *beacon)
{
    for (int index = 0; index < scanner->size; index++)
        if (scanner->beacons[index][0] == beacon[0]
            && scanner->beacons[index][1] == beacon[1]
            && scanner->beacons[index][2] == beacon[2])
            return;
    if (scanner->size == scanner->capacity)
        scanner->beacons = realloc(scanner->beacons, (scanner->capacity += LIST_INCREMENT) * sizeof(Beacon));
    scanner->beacons[scanner->size][0] = beacon[0];
    scanner->beacons[scanner->size][1] = beacon[1];
    scanner->beacons[scanner->size][2] = beacon[2];
    scanner->size++;
}

#define TEST_SPACE_SIZE 6
int TEST_SPACE[TEST_SPACE_SIZE][2] = { { 0,1 }, { 1,1 }, { 2,1 }, { 0,-1 }, { 1,-1 }, { 2,-1 } };
int tryOverlap(BeaconList *known, BeaconList *candidate, Beacon offset)
{
    int product_size = known->size * candidate->size;
    int rotateDimensions[3];
    int rotateOffsets[3];
    for (int dimension = 0; dimension < 3; dimension++)
    {
        int overlapFound = 0;
        for (int testIndex = 0; testIndex < TEST_SPACE_SIZE; testIndex++)
        {
            int testDimension = TEST_SPACE[testIndex][0];
            int testOffset = TEST_SPACE[testIndex][1];
            Counter counter = (Counter) {
                malloc(product_size * sizeof(int)),
                calloc(product_size, sizeof(int)),
                0
            };
            for (int knownIndex = 0; knownIndex < known->size; knownIndex++)
                for (int candidateIndex = 0; candidateIndex < candidate->size; candidateIndex++)
                    addToCounter(&counter, candidate->beacons[candidateIndex][testDimension] * testOffset - known->beacons[knownIndex][dimension]);
            int mostCommonCount = 0;
            int mostCommonDifference = 0;
            for (int counterIndex = 0; counterIndex < counter.size; counterIndex++)
                if (counter.counts[counterIndex] > mostCommonCount)
                {
                    mostCommonCount = counter.counts[counterIndex];
                    mostCommonDifference = counter.differences[counterIndex];
                }
            free(counter.differences);
            free(counter.counts);
            if (mostCommonCount > 11)
            {
                overlapFound = 1;
                offset[dimension] = mostCommonDifference;
                rotateDimensions[dimension] = testDimension;
                rotateOffsets[dimension] = testOffset;
            }
            if (overlapFound)
                break;
        }
        if (!overlapFound)
            return 0;
    }
    for (int candidateIndex = 0; candidateIndex < candidate->size; candidateIndex++)
    {
        int x = candidate->beacons[candidateIndex][rotateDimensions[0]] * rotateOffsets[0] - offset[0];
        int y = candidate->beacons[candidateIndex][rotateDimensions[1]] * rotateOffsets[1] - offset[1];
        int z = candidate->beacons[candidateIndex][rotateDimensions[2]] * rotateOffsets[2] - offset[2];
        candidate->beacons[candidateIndex][0] = x;
        candidate->beacons[candidateIndex][1] = y;
        candidate->beacons[candidateIndex][2] = z;
    }
    return 1;
}

Results solve(Input input)
{
    BeaconList knownBeacons = (BeaconList) {
        malloc(LIST_INCREMENT * sizeof(Beacon)),
        0, LIST_INCREMENT
    };
    int *queue = calloc(input.size, sizeof(int));
    int *scannersDone = calloc(input.size, sizeof(int));
    queue[0] = scannersDone[0] = 1;
    Beacon *offsets = malloc(input.size * sizeof(Beacon));
    Beacon offset;
    offsets[0][0] = 0;
    offsets[0][1] = 0;
    offsets[0][2] = 0;
    int knownIndex;
    while ((knownIndex = nextInQueue(queue, input.size)) != EMPTY_QUEUE)
    {
        queue[knownIndex] = 0;
        for (int candidateIndex = 0; candidateIndex < input.size; candidateIndex++)
            if (!scannersDone[candidateIndex] && tryOverlap(&input.scanners[knownIndex], &input.scanners[candidateIndex], offset))
            {
                queue[candidateIndex] = scannersDone[candidateIndex] = 1;
                offsets[candidateIndex][0] = offset[0];
                offsets[candidateIndex][1] = offset[1];
                offsets[candidateIndex][2] = offset[2];
            }
        for (int beaconIndex = 0; beaconIndex < input.scanners[knownIndex].size; beaconIndex++)
            addToListUnique(&knownBeacons, input.scanners[knownIndex].beacons[beaconIndex]);
    }
    int maximum = -1;
    for (int leftIndex = 0; leftIndex < input.size; leftIndex++)
        for (int rightIndex = 0; rightIndex < input.size; rightIndex++)
        {
            int manhattan = 
                abs(offsets[leftIndex][0] - offsets[rightIndex][0]) +
                abs(offsets[leftIndex][1] - offsets[rightIndex][1]) +
                abs(offsets[leftIndex][2] - offsets[rightIndex][2]);
            maximum = maximum > manhattan ? maximum : manhattan;
        }
    free(queue);
    free(scannersDone);
    free(offsets);
    return (Results){knownBeacons.size, maximum};
}

BeaconList *addToInput(Input *input)
{
    if (input->size == input->capacity)
        input->scanners = realloc(input->scanners, (input->capacity += LIST_INCREMENT) * sizeof(BeaconList));
    input->scanners[input->size++] = (BeaconList) {
        malloc(LIST_INCREMENT * sizeof(Beacon)),
        0, LIST_INCREMENT
    };
    return &input->scanners[input->size - 1];
}

void addToList(BeaconList *scanner, int *beacon)
{
    if (scanner->size == scanner->capacity)
        scanner->beacons = realloc(scanner->beacons, (scanner->capacity += LIST_INCREMENT) * sizeof(Beacon));
    scanner->beacons[scanner->size][0] = beacon[0];
    scanner->beacons[scanner->size][1] = beacon[1];
    scanner->beacons[scanner->size][2] = beacon[2];
    scanner->size++;
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    Input input = {
        malloc(LIST_INCREMENT * sizeof(BeaconList)),
        0, LIST_INCREMENT
    };
    char *line = NULL;
    size_t len;
    BeaconList *scanner;
    int beacon[3];
    while (getline(&line, &len, file) != EOF)
    {
        if (line[1] == '-')
        {
            scanner = addToInput(&input);            
        } else if (line[0] != '\n')
        {
            sscanf(line, "%d,%d,%d", &beacon[0], &beacon[1], &beacon[2]);
            addToList(scanner, beacon);
        }
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.scanners);
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

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct
{
    char dependant, dependency;
} DependencyPair;

typedef struct
{
    int count, capacity;
    DependencyPair *pairs;
} Input;
typedef struct
{
    const char *part1;
    int part2;
} Results;

int stepToBit(char step)
{
    return 1 << (step - 'A');
}

int *buildDependencyGraph(Input input)
{
    int *dependencies = calloc(26, sizeof(int));
    while (input.count--)
    {
        dependencies[input.pairs->dependant - 'A'] |= stepToBit(input.pairs->dependency);
        input.pairs++;
    }
    return dependencies;
}

int allOn(int *removed)
{
    for (int dependant = 0; dependant < 26; dependant++)
        if (!removed[dependant])
            return 0;
    return 1;
}

char *part1(int *originalDependencies)
{
    int dependencies[26], removed[26], dependant;
    for (dependant = 0; dependant < 26; dependant++)
    {
        dependencies[dependant] = originalDependencies[dependant];
        removed[dependant] = 0;
    }
    char *path = malloc(27);
    path[26] = 0;
    int nextStep, pathIndex = 0;
    while (!allOn(removed))
    {
        nextStep = 0;
        while (1)
            if (dependencies[nextStep] == 0 && !removed[nextStep])
                break;
            else
                nextStep++;
        removed[nextStep] = 1;
        path[pathIndex++] = nextStep + 'A';
        for (dependant = 0; dependant < 26; dependant++)
            dependencies[dependant] &= ~(1 << nextStep);
    }
    return path;
}

int workerCount(int *workers)
{
    int count = 0;
    for (int step = 0; step < 26; step++)
        count += workers[step] > 0;
    return count;
}

int allOff(int *workers)
{
    for (int dependant = 0; dependant < 26; dependant++)
        if (workers[dependant])
            return 0;
    return 1;
}

int part2(int *dependencies)
{
    int removed[26], step, nextStep, dependant, workers[26];
    for (step = 0; step < 26; step++)
        removed[step] = workers[step] = 0;
    const int WORKER_COUNT = 5;
    const int STEP_DURATION_OFFSET = 'A' - 4;
    int seconds = 0;
    while (!allOn(removed) || !allOff(workers))
    {
        for (step = 0; step < 26; step++)
            if (workers[step] && !(--workers[step]))
                for (dependant = 0; dependant < 26; dependant++)
                    dependencies[dependant] &= ~(1 << step);
        step = 0;
        while (workerCount(workers) < WORKER_COUNT && step < 26)
        {
            if (dependencies[step] == 0 && !removed[step])
            {
                workers[step] = step + STEP_DURATION_OFFSET;
                removed[step] = 1;
            }
            step++;
        }
        seconds++;
    }
    return seconds - 1;
}

Results solve(Input input)
{
    int *dependencies = buildDependencyGraph(input);
    return (Results){part1(dependencies), part2(dependencies)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, char dependant, char dependency)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        DependencyPair *oldPairs = input->pairs;
        DependencyPair *newPairs = realloc(oldPairs, input->capacity * sizeof(DependencyPair));
        input->pairs = newPairs;
    }
    input->pairs[input->count++] = (DependencyPair){dependant, dependency};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    char *line;
    size_t lineLength;
    Input input = {
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(DependencyPair))};
    char dependant, dependency;
    while (getline(&line, &lineLength, file) != EOF)
    {
        sscanf(line, "Step %c must be finished before step %c can begin.", &dependency, &dependant);
        addToInput(&input, dependant, dependency);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.pairs);
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
    printf("P1: %s\n", results.part1);
    printf("P2: %d\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}
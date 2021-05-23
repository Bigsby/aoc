#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef int *List;
typedef struct
{
    int count, capacity;
    List numbers;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct
{
    int count, capacity;
    List *lists;
} PreviousLists;

int areListsEqual(List listA, List listB, int size)
{
    while (size--)
        if (*(listA++) != *(listB++))
            return 0;
    return 1;
}

#define LISTS_INCREMENT 10
#define NEW_LIST -1
int addToPreviousLists(PreviousLists *lists, int *list, int size)
{
    int index = 0;
    while (index < lists->count)
        if (areListsEqual(lists->lists[index++], list, size))
            return index;
    if (lists->count == lists->capacity)
    {
        lists->capacity += LISTS_INCREMENT;
        List *oldLists = lists->lists;
        List *newLists = realloc(oldLists, lists->capacity * (sizeof(List)));
        lists->lists = newLists;
    }
    lists->lists[lists->count] = calloc(size, sizeof(int));
    memcpy(lists->lists[lists->count++], list, size * sizeof(int));
    return NEW_LIST;
}

void freePreviousLists(PreviousLists previousLists)
{
    List *lists = previousLists.lists;
    while (previousLists.count--)
        free(*(lists++));
    free(previousLists.lists);
}

Results solve(Input input)
{
    int numbersLength = input.count;
    PreviousLists previousLists = {
        0, LISTS_INCREMENT,
        calloc(LISTS_INCREMENT, sizeof(List))};
    int cycles = 0, repeatIndex, updateIndex, maxNumber, index, testNumber;
    List currenList = input.numbers;
    while (1)
    {
        if ((repeatIndex = addToPreviousLists(&previousLists, currenList, numbersLength)) != NEW_LIST)
        {
            freePreviousLists(previousLists);
            return (Results){cycles, cycles - repeatIndex + 1};
        }
        cycles++;
        updateIndex = -1;
        maxNumber = 0;
        for (index = 0; index < numbersLength; index++)
            if ((testNumber = currenList[index]) > maxNumber)
            {
                maxNumber = testNumber;
                updateIndex = index;
            }
        currenList[updateIndex] = 0;
        while (maxNumber)
        {
            updateIndex++;
            currenList[updateIndex % numbersLength]++;
            maxNumber--;
        }
    }
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int number)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        int *oldNumbers = input->numbers;
        int *newNumbers = realloc(oldNumbers, input->capacity * sizeof(int));
        input->numbers = newNumbers;
    }
    input->numbers[input->count++] = number;
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
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(int))};
    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    rewind(file);
    char *content = malloc(length);
    fread(content, 1, length, file);
    char *value = strtok(content, "\t");
    while (value != NULL)
    {
        addToInput(&input, atoi(value));
        value = strtok(NULL, "\t");
    }
    free(content);
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.numbers);
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
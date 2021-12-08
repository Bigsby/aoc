#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct
{
    int peopleCount, answers[26];
} Group;

typedef struct
{
    int count, capacity;
    Group *groups;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int part1(Input input)
{
    int differentAnswers = 0, index;
    Group group;
    while (input.count--)
    {
        group = *(input.groups++);
        for (int index = 0; index < 26; index++)
            differentAnswers += group.answers[index] > 0;
    }
    return differentAnswers;
}

int part2(Input input)
{
    int commonAnswers = 0, index;
    Group group;
    while (input.count--)
    {
        group = *(input.groups++);
        for (int index = 0; index < 26; index++)
            commonAnswers += group.answers[index] == group.peopleCount;
    }
    return commonAnswers;
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, Group group)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->groups = realloc(input->groups, input->capacity * sizeof(Group));
    }
    input->groups[input->count++] = group;
}

Group newGroup()
{
    Group group;
    group.peopleCount = 0;
    for (int index = 0; index < 26; index++)
        group.answers[index] = 0;
    return group;
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
        malloc(INPUT_INCREMENT * sizeof(Group))};
    Group group = newGroup();
    char *line = NULL, *cursor, c;
    size_t lineLength;
    while (getline(&line, &lineLength, file) != EOF)
    {
        if (line[0] == '\n')
        {
            addToInput(&input, group);
            group = newGroup();
        }
        else
        {
            group.peopleCount++;
            cursor = line;
            while ((c = *(cursor++)) != '\n')
                group.answers[c - 'a']++;
        }
    }
    addToInput(&input, group);
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.groups);
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

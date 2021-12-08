#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

typedef struct
{
    char *name;
    int id;
    char *checksum;
} Room;

typedef struct
{
    Room *rooms;
    int count;
    int size;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int isRoomValid(const char *name, const char *checksum)
{
    int processedCount = 0, letterIndex, processedIndex, shiftFrom, previousValue, oldValue;
    int counts[26];
    for (letterIndex = 0; letterIndex < 26; letterIndex++)
        counts[letterIndex] = 0;
    char c;
    while ((c = *(name++)))
        if (c >= 'a')
            counts[c - 'a']++;
    char processed[5];
    for (letterIndex = 0; letterIndex < 26; letterIndex++)
    {
        shiftFrom = -1;
        for (processedIndex = 0; processedIndex < processedCount; processedIndex++)
            if (counts[letterIndex] > counts[processed[processedIndex]] ||
                (counts[letterIndex] == counts[processed[processedIndex]] && letterIndex < processed[processedIndex]))
            {
                shiftFrom = processedIndex;
                break;
            }
        if (shiftFrom != -1)
        {
            processedCount++;
            previousValue = letterIndex;
            for (; processedIndex < processedCount && processedIndex < 5; processedIndex++)
            {
                oldValue = processed[processedIndex];
                processed[processedIndex] = previousValue;
                previousValue = oldValue;
            }
        }
        else if (processedCount < 5)
            processed[processedCount++] = letterIndex;
    }
    for (int processedIndex = 0; processedIndex < 5; processedIndex++)
        processed[processedIndex] += 'a';
    return strncmp(processed, checksum, 5) == 0;
}

int part1(Input input)
{
    int total = 0;
    while (input.count--)
    {
        if (isRoomValid(input.rooms->name, input.rooms->checksum))
            total += input.rooms->id;
        input.rooms++;
    }
    return total;
}

char getNextChar(char c)
{
    switch (c)
    {
    case '-':
    case ' ':
        return ' ';
    case 'z':
        return 'a';
    default:
        return c + 1;
    }
}

void rotateName(char *name, int count)
{
    while (count--)
    {
        int index = 0;
        char c;
        while ((c = name[index]) != 0)
            name[index++] = getNextChar(c);
    }
}

const char *SEARCH_NAME = "northpole object storage";
int part2(Input input)
{
    while (input.count--)
    {
        if (isRoomValid(input.rooms->name, input.rooms->checksum))
        {
            rotateName(input.rooms->name, input.rooms->id);
            if (strcmp(SEARCH_NAME, input.rooms->name) == 0)
                return input.rooms->id;
        }
        input.rooms++;
    }
    return -1;
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, char *name, int id, char *checksum)
{
    if (input->count == input->size)
    {
        input->size += INPUT_INCREMENT;
        input->rooms = realloc(input->rooms, input->size * sizeof(Room));
    }
    input->rooms[input->count++] = (Room){name, id, checksum};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    regex_t regexCompiled;
    regmatch_t groupArray[4];
    if (regcomp(&regexCompiled, "^([a-z\\-]+)-([0-9]+)\\[([a-z]+)\\]", REG_EXTENDED))
    {
        perror("Error compiling regex.");
        exit(1);
    }
    size_t lineLength;
    char *line = NULL, *cursor = NULL;
    Input input = {
        calloc(INPUT_INCREMENT, sizeof(Room)),
        0,
        INPUT_INCREMENT};
    char *name, *checksum;
    int id, group, groupLength;
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        while (!regexec(&regexCompiled, cursor, 4, groupArray, 0))
        {
            for (group = 0; group <= 3 && groupArray[group].rm_so != -1; group++)
            {
                groupLength = strlen(cursor) + 1;
                char cursorCopy[groupLength];
                strcpy(cursorCopy, cursor);
                cursorCopy[groupArray[group].rm_eo] = 0;
                switch (group)
                {
                case 1:
                    name = malloc(groupLength);
                    strcpy(name, cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    id = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 3:
                    checksum = malloc(groupLength);
                    strcpy(checksum, cursorCopy + groupArray[group].rm_so);
                }
            }
            cursor += groupArray[0].rm_eo;
        }
        addToInput(&input, name, id, checksum);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    Room *rooms = input.rooms;
    while (input.count--)
    {
        free(rooms->name);
        free(rooms->checksum);
        rooms++;
    }
    free(input.rooms);
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

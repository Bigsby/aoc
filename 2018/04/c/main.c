#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

typedef struct GuardNode
{
    int id, total, minutes[60];
    struct GuardNode *left, *right;
} GuardNode;

typedef struct
{
    int year, month, day, hour, minute;
    char *message;
} LogRecord;

typedef struct
{
    LogRecord *records;
    int count, size;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

GuardNode *addToGuardsIfNotPresent(GuardNode *node, int id)
{
    if (node == NULL)
    {
        node = malloc(sizeof(GuardNode));
        node->id = id;
        node->left = node->right = NULL;
        node->total = 0;
        for (int minute = 0; minute < 60; minute++)
            node->minutes[minute] = 0;
    }
    else if (node->id > id)
        node->left = addToGuardsIfNotPresent(node->left, id);
    else if (node->id < id)
        node->right = addToGuardsIfNotPresent(node->right, id);
    return node;
}

GuardNode *getGuardRecord(GuardNode *node, int id)
{
    if (node == NULL)
        return NULL;
    if (node->id == id)
        return node;
    if (node->id > id)
        return getGuardRecord(node->left, id);
    return getGuardRecord(node->right, id);
}

void getMaxTotal(GuardNode *node, int *max, int *id)
{
    if (node == NULL)
        return;
    if (node->total > *max)
    {
        *id = node->id;
        *max = node->total;
    }
    getMaxTotal(node->left, max, id);
    getMaxTotal(node->right, max, id);
}

int part1(GuardNode *guards)
{
    int max = 0, guardId;
    getMaxTotal(guards, &max, &guardId);
    GuardNode *guard = getGuardRecord(guards, guardId);
    int maxTotal = 0, maxMinute;
    for (int minute = 0; minute < 60; minute++)
        if (guard->minutes[minute] > maxTotal)
        {
            maxTotal = guard->minutes[minute];
            maxMinute = minute;
        }
    return guardId * maxMinute;
}

void getMaxMinuteTotal(GuardNode *node, int *max, int *maxMinute, int *id)
{
    if (node == NULL)
        return;
    for (int minute = 0; minute < 60; minute++)
        if (node->minutes[minute] > *max)
        {
            *max = node->minutes[minute];
            *maxMinute = minute;
            *id = node->id;
        }
    getMaxMinuteTotal(node->left, max, maxMinute, id);
    getMaxMinuteTotal(node->right, max, maxMinute, id);
}

int part2(GuardNode *guards)
{
    int maxTotal = 0, maxMinute = -1, guardId;
    getMaxMinuteTotal(guards, &maxTotal, &maxMinute, &guardId);
    return guardId * maxMinute;
}

int compare(int a, int b)
{
    return (a < b) - (b < a);
}

int greaterThan(LogRecord log1, LogRecord log2)
{
    int comp = compare(log1.year, log2.year);
    if (comp == -1)
        return 1;
    if (comp == 1)
        return 0;
    comp = compare(log1.month, log2.month);
    if (comp == -1)
        return 1;
    if (comp == 1)
        return 0;
    comp = compare(log1.day, log2.day);
    if (comp == -1)
        return 1;
    if (comp == 1)
        return 0;
    comp = compare(log1.hour, log2.hour);
    if (comp == -1)
        return 1;
    if (comp == 1)
        return 0;
    return compare(log1.minute, log2.minute) == -1;
}

void sort(Input input)
{
    int i, j;
    LogRecord temp;
    for (i = 0; i < input.count - 1; i++)
        for (j = 0; j < input.count - 1 - i; j++)
            if (greaterThan(input.records[j], input.records[j + 1]))
            {
                temp = input.records[j];
                input.records[j] = input.records[j + 1];
                input.records[j + 1] = temp;
            }
}

void recordGuardTimes(GuardNode *guards, int guardId, int lastAsleep, int woke)
{
    GuardNode *guardRecord = getGuardRecord(guards, guardId);
    for (; lastAsleep < woke; lastAsleep++)
    {
        guardRecord->total++;
        guardRecord->minutes[lastAsleep]++;
    }
}

GuardNode *buildRecords(Input input)
{
    const char *FALL_ASLEEP = "falls asleep", *WAKE_UP = "wakes up";
    sort(input);
    GuardNode *guards = NULL;
    int guardId = 0, newGuardId = 0, guardAsleep = 0, lastAsleep = 0;
    while (input.count--)
    {
        if (strcmp(input.records->message, FALL_ASLEEP) == 0)
        {
            lastAsleep = input.records->minute;
            guardAsleep = 1;
        }
        else if (strcmp(input.records->message, WAKE_UP) == 0)
        {
            guardAsleep = 0;
            recordGuardTimes(guards, guardId, lastAsleep, input.records->minute);
        }
        else if (sscanf(input.records->message, "Guard #%d begins shift", &newGuardId))
        {
            if (guardAsleep)
            {
                recordGuardTimes(guards, guardId, lastAsleep, 60);
                guardAsleep = 0;
            }
            guardId = newGuardId;
            guards = addToGuardsIfNotPresent(guards, guardId);
        }
        input.records++;
    }
    return guards;
}

Results solve(Input input)
{
    GuardNode *guards = buildRecords(input);
    return (Results){part1(guards), part2(guards)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, LogRecord record)
{
    if (input->count == input->size)
    {
        input->size += INPUT_INCREMENT;
        input->records = realloc(input->records, input->size * sizeof(LogRecord));
    }
    input->records[input->count++] = record;
}

char *rtrim(char *str, const char *seps)
{
    int i;
    if (seps == NULL)
        seps = "\t\n\v\f\r ";
    i = strlen(str) - 1;
    while (i >= 0 && strchr(seps, str[i]) != NULL)
        str[i--] = '\0';
    return str;
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
    regmatch_t groupArray[7];
    if (regcomp(&regexCompiled, "\\[([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})\\] (.*)$", REG_EXTENDED))
    {
        perror("Error compiling regex.");
        exit(1);
    }
    Input input = {
        calloc(INPUT_INCREMENT, sizeof(LogRecord)),
        0,
        INPUT_INCREMENT};
    char *line = NULL, *cursor = NULL, *message;
    size_t lineLength;
    int group, groupLength, year, month, day, hour, minute;
    while (getline(&line, &lineLength, file) != EOF)
    {
        cursor = line;
        if (!regexec(&regexCompiled, cursor, 7, groupArray, 0))
        {
            for (group = 0; group <= 6 && groupArray[group].rm_so != -1; group++)
            {
                groupLength = strlen(cursor) + 1;
                char cursorCopy[groupLength];
                strcpy(cursorCopy, cursor);
                cursorCopy[groupArray[group].rm_eo] = 0;
                switch (group)
                {
                case 1:
                    year = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    month = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 3:
                    day = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 4:
                    hour = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 5:
                    minute = atoi(cursorCopy + groupArray[group].rm_so);
                    break;
                case 6:
                    message = malloc(groupLength);
                    strcpy(message, cursorCopy + groupArray[group].rm_so);
                    rtrim(message, NULL);
                }
            }
            cursor += groupArray[0].rm_eo;
            addToInput(&input, (LogRecord){year, month, day, hour, minute, message});
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

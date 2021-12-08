#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <math.h>

typedef char Connection[14];
typedef struct {
    Connection *connections;
    int count, capacity;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int getBitCount(char wire)
{
    int count = 0;
    while (wire)
    {
        count += wire & 1;
        wire >>= 1;
    }
    return count;
}

int part1(Input input)
{
    int count = 0;
    while (input.count--)
    {
        for (int wire = 10; wire < 14; wire++)
        {
            int wireCount = getBitCount((*input.connections)[wire]);
            switch (wireCount)
            {
                case 2:
                case 3:
                case 4:
                case 7:
                    count++;
                    break;
            }
        }
        input.connections++;
    }
    return count;
}

void filterAndRemove(Connection connection, char *digits, char digit, int digitLength, char exceptDigit, char exceptLength)
{
    for (int wire = 0; wire < 10; wire++)
    {
        char segments = connection[wire];
        if (!segments)
            continue;
        char length = getBitCount(segments);
        if (length == digitLength && (!exceptLength || getBitCount(segments & ~digits[exceptDigit]) == exceptLength))
        {
            digits[digit] = segments;
            connection[wire] = 0;
            return;
        }
    }
    perror("Digit not found");
    exit(1);
}

int getConnectionNumber(Connection connection)
{
    char digits[10] = { 0 };
    filterAndRemove(connection, digits, 7, 3, 0, 0);
    filterAndRemove(connection, digits, 4, 4, 0, 0);
    filterAndRemove(connection, digits, 1, 2, 0, 0);
    filterAndRemove(connection, digits, 8, 7, 0, 0);
    filterAndRemove(connection, digits, 3, 5, 1, 3);
    filterAndRemove(connection, digits, 6, 6, 1, 5);
    filterAndRemove(connection, digits, 2, 5, 4, 3);
    filterAndRemove(connection, digits, 5, 5, 4, 2);
    filterAndRemove(connection, digits, 0, 6, 4, 3);
    for (int wire = 0; wire < 10; wire++)
        if (connection[wire])
            digits[9] = connection[wire];
    int total = 0;
    for (int display = 0; display < 4; display++)
        for (int digit = 0; digit < 10; digit++)
            if (connection[display + 10] == digits[digit])
                total += digit * ((int)pow(10, 3 - display));
    return total;
}

int part2(Input input)
{
    int total = 0;
    while (input.count--)
        total += getConnectionNumber(*input.connections++);
    return total;
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, Connection connection)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->connections = realloc(input->connections, input->capacity * sizeof(Connection));
    }
    memcpy(input->connections[input->count++], connection, sizeof(Connection));
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
        malloc(INPUT_INCREMENT * sizeof(Connection)),
        0, INPUT_INCREMENT
    };
    char *line = NULL, *wire;
    size_t len;
    while (getline(&line, &len, file) != EOF)
    {
        Connection connection;
        int index = 0;
        wire = strtok(line, " ");
        while (wire != NULL)
        {
            if (*wire != '|')
            {
                char segments = 0;
                while (*wire)
                    segments |= 1 << (*wire++ - 'a');
                connection[index++] = segments;
            }
            wire = strtok(NULL, " ");
        }
        addToInput(&input, connection);
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

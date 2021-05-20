#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef char *Input;
typedef struct
{
    char *part1;
    char *part2;
} Results;

typedef struct
{
    int x;
    int y;
} Position;

typedef struct
{
    Position position;
    char digit;
} Key;

#define CODE_MAXSIZE 10
#define KEYPAD_OUT 0
#define KEYPAD1_SIZE 9
#define KEYPAD2_SIZE 13

Key KEYPAD1[] = {
    {{-1, -1}, '1'}, {{0, -1}, '2'}, {{1, -1}, '3'},
    {{-1,  0}, '4'}, {{0,  0}, '5'}, {{1,  0}, '6'},
    {{-1,  1}, '7'}, {{0,  1}, '8'}, {{1,  1}, '9'},
};

Key KEYPAD2[] = {
                                     {{0, -2}, '1'},
                    {{-1, -1}, '2'}, {{0, -1}, '3'}, {{1, -1}, '4'},
    {{-2, 0}, '5'}, {{-1,  0}, '6'}, {{0,  0}, '7'}, {{1,  0}, '8'}, {{2, 0}, '9'},
                    {{-1,  1}, 'A'}, {{0,  1}, 'B'}, {{1,  1}, 'C'},
                                     {{0,  2}, 'D'},
};

int positionEquals(Position a, Position b)
{
    return (a.x == b.x) && (a.y == b.y);
}

Position positionAdd(Position a, int x, int y)
{
    return (Position){
        a.x + x,
        a.y + y};
}

char getDigit(Position position, Key *keypad, int size)
{
    for (; --size; keypad++)
        if (positionEquals(keypad->position, position))
            return keypad->digit;
    return KEYPAD_OUT;
}

void getCode(char *code, Input paths, Key *keypad, int size)
{
    size++;
    int index = 0;
    Position position = {0, 0}, oldPosition;
    char digit, lastDigit;
    while (*paths)
    {
        oldPosition = position;
        switch (*paths)
        {
        case 'D':
            position = positionAdd(position, 0, 1);
            break;
        case 'U':
            position = positionAdd(position, 0, -1);
            break;
        case 'L':
            position = positionAdd(position, -1, 0);
            break;
        case 'R':
            position = positionAdd(position, 1, 0);
            break;
        }
        if ((digit = getDigit(position, keypad, size)) == KEYPAD_OUT)
            position = oldPosition;
        else
            lastDigit = digit;
        if (*++paths == '\n')
            code[index++] = lastDigit;
    }
    code[index] = '\0';
}

Results solve(Input input)
{
    char *code1 = malloc(CODE_MAXSIZE);
    char *code2 = malloc(CODE_MAXSIZE);
    getCode(code1, input, KEYPAD1, KEYPAD1_SIZE);
    getCode(code2, input, KEYPAD2, KEYPAD2_SIZE);
    return (Results){code1, code2};
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
    char *paths = calloc(1, length + 1);
    size_t read;
    fread(paths, length, 1, file);
    fclose(file);
    return paths;
}

void freeInput(Input input)
{
    free(input);
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
    printf("P2: %s\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}
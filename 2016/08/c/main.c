#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>

typedef enum {
    RECT,
    ROW,
    COLUMN
} InstructionType;
typedef struct {
    InstructionType type;
    int a, b;
} Instruction;

typedef struct {
    int count, capacity;
    Instruction *instructions;
} Input;
typedef struct
{
    int part1;
    char *part2;
} Results;

#define SCREEN_WIDTH 50
#define SCREEN_HEIGHT 6
#define CHARACTER_WIDTH 5
typedef char **Screen;

Screen initializeScreen()
{
    Screen screen = calloc(SCREEN_WIDTH, sizeof(char*));
    for (int i = 0; i < SCREEN_WIDTH; i++)
        screen[i] = calloc(SCREEN_HEIGHT, sizeof(char));
    return screen;
}

void printScreen(const Screen screen)
{
    for (int y = 0; y < SCREEN_HEIGHT; y++)
    {
        for (int x = 0; x < SCREEN_WIDTH; x++)
            printf("%c", screen[x][y] ? '#' : '.');
        printf("\n");
    }
}

Screen runInstructions(Input input)
{
    Screen screen = initializeScreen();
    int x, y;
    char replaceRow[SCREEN_WIDTH], replaceColumn[SCREEN_HEIGHT];
    while (input.count--)
    {
        switch (input.instructions->type)
        {
            case RECT:
                
                for (x = 0; x < input.instructions->a; x++)
                    for (y = 0; y < input.instructions->b; y++)
                        screen[x][y] = 1;
                break;
            case ROW:
                for (x = 0; x < SCREEN_WIDTH; x++)
                    replaceRow[x] = screen[(x - input.instructions->b + SCREEN_WIDTH) % SCREEN_WIDTH][input.instructions->a];
                for (x = 0; x < SCREEN_WIDTH; x++)
                    screen[x][input.instructions->a] = replaceRow[x];
                break;
            case COLUMN:
                for (y = 0; y < SCREEN_HEIGHT; y++)
                    replaceColumn[y] = screen[input.instructions->a][(y - input.instructions->b + SCREEN_HEIGHT) % SCREEN_HEIGHT];
                for (y = 0; y < SCREEN_HEIGHT; y++)
                    screen[input.instructions->a][y] = replaceColumn[y];
                break;
        }
        input.instructions++;
    }
    return screen;
}

int countPixels(Screen screen)
{
    int total = 0, x, y;
    for (x = 0; x < SCREEN_WIDTH; x++)
        for (y = 0; y < SCREEN_HEIGHT; y++)
            total += screen[x][y];
    return total;
}

#define A \
    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b11110 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5)
#define B \
    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b11100 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b11100 << CHARACTER_WIDTH * 5)
#define C \
    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5)
#define D \
    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b11100 << CHARACTER_WIDTH * 5)
#define E \
    (0b11110 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b11100 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b11110 << CHARACTER_WIDTH * 5)
#define F \
    (0b11110 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b11100 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b10000 << CHARACTER_WIDTH * 5)
#define G \
    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b10110 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01110 << CHARACTER_WIDTH * 5)
#define H \
    (0b10010 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b11110 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5)
#define I \
    (0b01110 << CHARACTER_WIDTH * 0) + \
    (0b00100 << CHARACTER_WIDTH * 1) + \
    (0b00100 << CHARACTER_WIDTH * 2) + \
    (0b00100 << CHARACTER_WIDTH * 3) + \
    (0b00100 << CHARACTER_WIDTH * 4) + \
    (0b01110 << CHARACTER_WIDTH * 5)
#define J \
    (0b00110 << CHARACTER_WIDTH * 0) + \
    (0b00010 << CHARACTER_WIDTH * 1) + \
    (0b00010 << CHARACTER_WIDTH * 2) + \
    (0b00010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5)
#define K \
    (0b10010 << CHARACTER_WIDTH * 0) + \
    (0b10100 << CHARACTER_WIDTH * 1) + \
    (0b11000 << CHARACTER_WIDTH * 2) + \
    (0b10100 << CHARACTER_WIDTH * 3) + \
    (0b10100 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5)
#define L \
    (0b10000 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b11110 << CHARACTER_WIDTH * 5)
#define M 0
#define N 0
#define O \
    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5)
#define P \
    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b11100 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b10000 << CHARACTER_WIDTH * 5)
#define Q 0
#define R \
    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b11100 << CHARACTER_WIDTH * 3) + \
    (0b10100 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5)
#define S \
    (0b01110 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b01100 << CHARACTER_WIDTH * 3) + \
    (0b00010 << CHARACTER_WIDTH * 4) + \
    (0b11100 << CHARACTER_WIDTH * 5)
#define T 0
#define U \
    (0b10010 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5)
#define V 0
#define W 0
#define X 0
#define Y \
    (0b10001 << CHARACTER_WIDTH * 0) + \
    (0b10001 << CHARACTER_WIDTH * 1) + \
    (0b01010 << CHARACTER_WIDTH * 2) + \
    (0b00100 << CHARACTER_WIDTH * 3) + \
    (0b00100 << CHARACTER_WIDTH * 4) + \
    (0b00100 << CHARACTER_WIDTH * 5)
#define Z \
    (0b11110 << CHARACTER_WIDTH * 0) + \
    (0b00010 << CHARACTER_WIDTH * 1) + \
    (0b00100 << CHARACTER_WIDTH * 2) + \
    (0b01000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b11110 << CHARACTER_WIDTH * 5)
const int LETTERS[] = { A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z };
char getLetter(int value)
{
    for (int index = 0; index < 26; index++)
        if (LETTERS[index] == value)
            return 'A' + index;
    perror("Unknow character");
    exit(1);
}

char *getCode(Screen screen)
{
    int screenValue, x, y;
    char *code = calloc((SCREEN_WIDTH / CHARACTER_WIDTH) + 1, 1);
    for (int index = 0; index < SCREEN_WIDTH / CHARACTER_WIDTH; index++)
    {
        screenValue = 0;
        for (x = 0; x < CHARACTER_WIDTH; x++)
            for (y = 0; y < SCREEN_HEIGHT; y++)
                screenValue += screen[CHARACTER_WIDTH * index + x][y] * ((int)pow(2, CHARACTER_WIDTH - 1 - x) << (y * CHARACTER_WIDTH));
        code[index] = getLetter(screenValue);
    }
    return code;
}

Results solve(Input input)
{
    Screen screen = runInstructions(input);
    return (Results){countPixels(screen), getCode(screen)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, InstructionType type, int a, int b)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        input->instructions = realloc(input->instructions, input->capacity * sizeof(Instruction));
    }
    input->instructions[input->count++] = (Instruction){type, a, b};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    char *line = NULL;
    size_t lineLength;
    Input input = {
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(Instruction))
    };
    int a, b;
    while (getline(&line, &lineLength, file) != EOF)
    {
        InstructionType type;
        if (sscanf(line, "rect %dx%d", &a, &b) == 2)
            type = RECT;
        else if (sscanf(line, "rotate row y=%d by %d", &a, &b) == 2)
            type = ROW;
        else if (sscanf(line, "rotate column x=%d by %d", &a, &b) == 2)
            type = COLUMN;
        else
        {
            perror("Unrecognized instruction\n");
            perror(line);
            exit(1);
        }
        addToInput(&input, type, a, b);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.instructions);
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
    printf("P2: %s\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}

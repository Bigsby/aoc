#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>

typedef struct {
    int count, *pixels;
} Input;
typedef struct
{
    int part1;
    char *part2;
} Results;

#define IMAGE_WIDTH 25
#define IMAGE_HEIGHT 6
#define PIXELS_PER_LAYER (IMAGE_WIDTH * IMAGE_HEIGHT)
#define CHARACTER_WIDTH 5

int part1(Input input)
{
    int layerCount = input.count / PIXELS_PER_LAYER;
    int leastZeros = PIXELS_PER_LAYER, zeros, ones, twos, index, result;
    for (int layerIndex = 0; layerIndex < layerCount; layerIndex++)
    {
        zeros = ones = twos = 0;
        for (index = 0; index < PIXELS_PER_LAYER; index++)
            switch (input.pixels[layerIndex * PIXELS_PER_LAYER + index])
            {
                case 0: zeros++; break;
                case 1: ones++; break;
                case 2: twos++; break;
            }
        if (zeros < leastZeros)
        {
            leastZeros = zeros;
            result = ones * twos;
        }
    }
    return result;
}

#define BLACK 0
#define WHITE 1
#define TRANSPARENT 2

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

void printImage(int *image)
{
    for (int y = 0; y < IMAGE_HEIGHT; y++)
    {
        for (int x = 0; x < IMAGE_WIDTH; x++)
            printf("%c", image[x + IMAGE_WIDTH * y] == WHITE ? '#' : '.');
        printf("\n");
    }
    printf("\n");
}

char *part2(Input input)
{
    int index, x, y, imageValue;
    int layerCount = input.count / PIXELS_PER_LAYER;
    int *image = malloc(PIXELS_PER_LAYER * sizeof(int));
    for (index = 0; index < PIXELS_PER_LAYER; index++)
        image[index] = TRANSPARENT;
    for (int layerIndex = 0; layerIndex < layerCount; layerIndex++)
        for (index = 0; index < PIXELS_PER_LAYER; index++)
        {
            if (image[index] < TRANSPARENT)
                continue;
            image[index] = input.pixels[layerIndex * PIXELS_PER_LAYER + index];
        }
    char *message = calloc((IMAGE_WIDTH / CHARACTER_WIDTH) + 1, 1);
    for (index = 0; index < IMAGE_WIDTH / CHARACTER_WIDTH; index++)
    {
        imageValue = 0;
        for (x = 0; x < CHARACTER_WIDTH; x++)
            for (y = 0; y < IMAGE_HEIGHT; y++)
                imageValue += (image[CHARACTER_WIDTH * index + x + IMAGE_WIDTH * y] == WHITE) * ((int)pow(2, CHARACTER_WIDTH - 1 - x) << (y * CHARACTER_WIDTH));
        message[index] = getLetter(imageValue);
    }
    return message;
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
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
    Input input = {
        (int)length - 1,
        malloc(length * sizeof(int))
    };
    char c;
    int *pixels = input.pixels;
    while ((c = fgetc(file)) != EOF)
        *(pixels++) = c - '0';
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.pixels);
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

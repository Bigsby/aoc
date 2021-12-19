#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct {
    int *elements;
    int size, capacity;
} Number;
typedef struct {
    Number *numbers;
    int size, capacity;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

#define OPEN -1
#define CLOSE -2
#define NO_NEXT -1

int getNextNumber(Number *number, int index, int direction)
{
    while (index > 0 && index < number->size)
    {
        if (number->elements[index] >= 0)
            return index;
        index += direction;
    }
    return NO_NEXT;
}

int explode(Number *number)
{
    int nest = 0;
    for (int index = 0; index < number->size; index++)
    {
        if (number->elements[index] == OPEN)
        {
            nest++;
            if (nest == 5)
            {
                int leftNumberIndex = getNextNumber(number, index, -1);
                int rightNumberIndex = getNextNumber(number, index + 3, 1);
                if (leftNumberIndex != NO_NEXT)
                    number->elements[leftNumberIndex] += number->elements[index + 1];
                if (rightNumberIndex != NO_NEXT)
                    number->elements[rightNumberIndex] += number->elements[index + 2];
                number->elements[index] = 0;
                index += 1;
                while (index < number->size - 2)
                {
                    number->elements[index] = number->elements[index + 3];
                    index++;
                }
                number->size -= 3;
                return 1;
            }
        } else if (number->elements[index] == CLOSE)
            nest--;
    }
    return 0;
}

int split(Number *number)
{
    for (int index = 0; index < number->size; index++)
        if (number->elements[index] > 9)
        {
            int left = number->elements[index] / 2;
            int right = number->elements[index] - left;
            if (number->capacity < number->size + 3)
                number->elements = realloc(number->elements, (number->capacity += 5) * sizeof(int));
            for (int move = number->size - 1; move > index; move--)
                number->elements[move + 3] = number->elements[move];
            number->elements[index++] = OPEN;
            number->elements[index++] = left;
            number->elements[index++] = right;
            number->elements[index++] = CLOSE;
            number->size += 3;
            return 1;
        }
    return 0;
}

Number reduce(Number number)
{
    Number result = {
        malloc(number.size * sizeof(int)),
        number.size,
        number.size
    };
    memcpy(result.elements, number.elements, number.size * sizeof(int));
    int changed = 1;
    while (changed)
    {
        changed = 0;
        changed = explode(&result);
        if (!changed)
            changed = split(&result);
    }
    return result;
}

int getMagnitude(Number number)
{
    while (number.size > 1)
        for (int index = 0; index < number.size; index++)
            if (number.elements[index] >= 0 && number.elements[index + 1] >= 0)
            {
                number.elements[index - 1] = number.elements[index] * 3 + number.elements[index + 1] * 2;
                while (index < number.size - 3)
                {
                    number.elements[index] = number.elements[index + 3];
                    index++;
                }
                number.size -= 3;
            }
    return number.elements[0];
}

Number reduceNumbers(Number left, Number right)
{
    int newSize = (left.size + right.size + 2);
    Number joined = {
        malloc(newSize * sizeof(int)),
        newSize, newSize
    };
    joined.elements[0] = OPEN;
    memcpy(joined.elements + 1, left.elements, left.size * sizeof(int));
    memcpy(joined.elements + 1 + left.size, right.elements, right.size * sizeof(int));
    joined.elements[left.size + right.size + 1] = CLOSE;
    return reduce(joined);
}

int part1(Input input)
{
    Number number = input.numbers[0];
    for (int index = 1; index < input.size; index++)
        number = reduceNumbers(number, input.numbers[index]);
    int magnitude = getMagnitude(number);
    free(number.elements);
    return magnitude;
}

int part2(Input input)
{
    int maximum = 0;
    for (int left = 0; left < input.size; left++)
        for (int right = 0; right < input.size; right++)
            if (left != right)
            {
                Number number = reduceNumbers(input.numbers[left], input.numbers[right]);
                int magnitude = getMagnitude(number);
                free(number.elements);
                maximum = maximum > magnitude ? maximum : magnitude;
            }
    return maximum;
}

Results solve(Input input)
{
    return (Results){part1(input), part2(input)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, Number number)
{
    if (input->size == input->capacity)
        input->numbers = realloc(input->numbers, (input->capacity += INPUT_INCREMENT) * sizeof(Number));
    input->numbers[input->size++] = (Number) { number.elements, number.size, number.capacity };
}

int encodeElement(char c)
{
    int result = c - '0';
    switch (c)
    {
        case '[':
            result = OPEN;
            break;
        case ']':
            result = CLOSE;
            break;
    }
    return result;
}

void addToNumber(Number *number, char c)
{
    if (number->size == number->capacity)
        number->elements = realloc(number->elements, (number->capacity += INPUT_INCREMENT) * sizeof(int));
    number->elements[number->size++] = encodeElement(c);
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    char *line = NULL, *cursor, c;
    size_t len;
    Input input = {
        malloc(INPUT_INCREMENT * sizeof(Number)),
        0, INPUT_INCREMENT
    };
    Number number;
    while (getline(&line, &len, file) != EOF)
    {
        number = (Number) {
            malloc(INPUT_INCREMENT * sizeof(int)),
            0, INPUT_INCREMENT
        };
        cursor = line;
        
        while ((c = *cursor++) != '\0')
            if (c != ',' && c != '\n')
                addToNumber(&number, c);
        addToInput(&input, number);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    for (int index = 0; index < input.size; index++)
        free(input.numbers[index].elements);
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

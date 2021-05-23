#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct
{
    int count, capacity, *seats;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

void sort(Input input)
{
    int i, j;
    int temp;
    for (i = 0; i < input.count - 1; i++)
        for (j = 0; j < input.count - 1 - i; j++)
            if (input.seats[j] > input.seats[j + 1])
            {
                temp = input.seats[j];
                input.seats[j] = input.seats[j + 1];
                input.seats[j + 1] = temp;
            }
}

int part2(Input input)
{
    sort(input);
    int lastId = input.seats[0], currentId;
    while (input.count--)
    {
        currentId = *(input.seats++);
        if (currentId - lastId == 2)
            return lastId + 1;
        lastId = currentId;
    }
    perror("Seat not found");
    exit(1);
}

int max(Input input)
{
    int max = 0, seat;
    while (input.count--)
        max = (seat = *(input.seats++)) > max ? seat : max;
    return max;
}

Results solve(Input input)
{
    return (Results){max(input), part2(input)};
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, int seat)
{
    if (input->count == input->capacity)
    {
        input->capacity += INPUT_INCREMENT;
        int *oldSeats = input->seats;
        int *newSeats = realloc(oldSeats, input->capacity * sizeof(int));
        input->seats = newSeats;
    }
    input->seats[input->count++] = seat;
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
        0,
        INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(int))};
    char *line = NULL, *cursor, c;
    size_t lineLength;
    int seat;
    while (getline(&line, &lineLength, file) != EOF)
    {
        seat = 0;
        cursor = line;
        while ((c = *(cursor++)) != 0)
        {
            switch (c)
            {
            case 'F':
            case 'L':
                seat <<= 1;
                break;
            case 'B':
            case 'R':
                seat <<= 1;
                seat |= 1;
                break;
            }
        }
        addToInput(&input, seat);
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input.seats);
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
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct {
    int chip, bot;
} ValueInstruction;
typedef struct {
    int bot, lowBot, low, highBot, high;
} GiveInstruction;
typedef struct {
    ValueInstruction *valueInstructions;
    int valueSize, valueCapacity;
    GiveInstruction *giveInstructions;
    int giveSize, giveCapacity;
    int maxBot;
    int maxOutput;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef struct {
    int low, high;
} Bot;


#define EMPTY -1

Bot *initializeBots(int maxBot)
{
    maxBot++;
    Bot *bots = malloc((maxBot) * sizeof(Bot));
    for (int index = 0; index < maxBot; index++)
        bots[index] = (Bot) { EMPTY, EMPTY };
    return bots;
}

void setBotChip(Bot *bots, int index, int chip)
{
    int low = bots[index].low;
    if (low == EMPTY)
        bots[index].low = chip;
    else if (chip > low)
        bots[index].high = chip;
    else
    {
        bots[index].low = chip;
        bots[index].high = low;
    }
}

int getNextCompleteBot(Bot *bots)
{
    int index = 0;
    while (1)
    {
        if (bots[index].low != EMPTY && bots[index] != EMPTY)
            return index;
        index++;
    }
    perror("No complete bots");
    exit(1);
}

Results solve(Input input)
{
    Bot *bots = initializeBots(input.maxBot);
    while (input.valueSize--)
    {
        ValueInstruction value = *(input.valueInstructions++);
        setBotChip(bots, value.bot, value.chip);
    }
    int *outputs = calloc(input.maxOutput + 1, sizeof(int));
    int part1Result = 0, part2Result = 0;
    while (!part1Result || !part2Result)
    {
        int nextIndex = getNextCompleteBot(bots);
        

    }

    return (Results){1, 2};
}

#define INPUT_INCREMENT 10
void addValueInstructionToInput(Input *input, int chip, int bot)
{
    if (input->valueSize == input->valueCapacity)
        input->valueInstructions = realloc(input->valueInstructions, (input->valueCapacity += INPUT_INCREMENT) * sizeof(ValueInstruction));
    input->valueInstructions[input->valueSize++] = (ValueInstruction) { chip, bot };
}

void addGiveInstructionToInput(Input *input, int bot, char *giveLow, int low, char *giveHigh, int high)
{
    // index instruction by bot as index
    if (input->giveSize == input->giveCapacity)
        input->giveInstructions = realloc(input->giveInstructions, (input->giveCapacity += INPUT_INCREMENT) * sizeof(GiveInstruction));
    input->giveInstructions[input->giveSize++] = (GiveInstruction) {
        bot,
        *giveLow == 'b',
        low,
        *giveHigh == 'b',
        high
    };
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
        malloc(INPUT_INCREMENT * sizeof(ValueInstruction)),
        0, INPUT_INCREMENT,
        malloc(INPUT_INCREMENT * sizeof(GiveInstruction)),
        0, INPUT_INCREMENT,
        0, 0
    };
    char *line = NULL;
    size_t len;
    int bot, chip, high, low;
    char giveLow[7], giveHigh[7];
    while (getline(&line, &len, file) != EOF)
    {
        if (line[0] == 'v')
        {
            sscanf(line, "value %d goes to bot %d", &chip, &bot);
            addValueInstructionToInput(&input, chip, bot);
        }
        else
        {
            sscanf(line, "bot %d gives low to %s %d and high to %s %d", &bot, giveLow, &low, giveHigh, &high);
            addGiveInstructionToInput(&input, bot, giveLow, low, giveHigh, high);
            if (*giveLow == 'o' && low > input.maxOutput)
                input.maxOutput = low;
            if (*giveHigh == 'o' && high > input.maxOutput)
                input.maxOutput = high;
        }
        if (bot > input.maxBot)
            input.maxBot = bot;
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

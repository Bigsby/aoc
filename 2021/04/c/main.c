#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

typedef struct {
    int numbers[5][5];
} Card;
typedef struct {
    int *numbers;
    int numbersCount, numbersCapacity;
    Card *cards;
    int cardsCount, cardsCapacity;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

int isCardComplete(Card card)
{
    for (int row = 0; row < 5; row++)
    {
        int rowComplete = 1;
        for (int column = 0; column < 5; column++)
            rowComplete &= card.numbers[row][column] < 0;
        if (rowComplete)
            return 1;
    }
    for (int column = 0; column < 5; column++)
    {
        int columnComplete = 1;
        for (int row = 0; row < 5; row++)
            columnComplete &= card.numbers[row][column] < 0;
        if (columnComplete)
            return 1;
    }
    return 0;
}

int getCardUnmarkedSum(Card card)
{
    int total = 0;
    for (int row = 0; row < 5; row++)
        for (int column = 0; column < 5; column++)
            if (card.numbers[row][column] > 0)
                total += card.numbers[row][column];
    return total;
}

int all(int *states, int count)
{
    while (count--)
        if (*states++ == 0)
            return 0;
    return 1;
}

int playGame(Input input, int first)
{
    Card *cards = malloc(sizeof(Card) * input.cardsCount);
    memcpy(cards, input.cards, sizeof(Card) * input.cardsCount);
    int *removedCards = calloc(input.cardsCount, sizeof(int));
    while (input.numbersCount--)
    {
        int number = *input.numbers++;
        for (int cardIndex = 0; cardIndex < input.cardsCount; cardIndex++)
        {
            for (int row = 0; row < 5; row++)
                for (int column = 0; column < 5; column++)
                {
                    if (cards[cardIndex].numbers[row][column] == number)
                    {
                        cards[cardIndex].numbers[row][column] = -100;
                        if (isCardComplete(cards[cardIndex]))
                        {
                            if (first)
                                return getCardUnmarkedSum(cards[cardIndex]) * number;
                            removedCards[cardIndex] = 1;
                            if (all(removedCards, input.cardsCount))
                                return getCardUnmarkedSum(cards[cardIndex]) * number;
                        }
                    }
                }
        }
    }
}

Results solve(Input input)
{
    return (Results){playGame(input, 1), playGame(input, 0)};
}

#define INPUT_INCREMENT 10
void addNumberToInput(Input *input, int number)
{
    if (input->numbersCount == input->numbersCapacity)
    {
        input->numbersCapacity += INPUT_INCREMENT;
        int *oldNumbers = input->numbers;
        int *newNumbers = realloc(oldNumbers, sizeof(int) * input->numbersCapacity);
        input->numbers = newNumbers;
    }
    input->numbers[input->numbersCount++] = number;
}

void addCardToInput(Input *input, Card card)
{
    if (input->cardsCount == input->cardsCapacity)
    {
        input->cardsCapacity += INPUT_INCREMENT;
        Card *oldCards = input->cards;
        Card *newCards = realloc(oldCards, sizeof(Card) * input->cardsCapacity);
        input->cards = newCards;
    }
    input->cards[input->cardsCount++] = card;
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
        malloc(sizeof(int) * INPUT_INCREMENT), 0, INPUT_INCREMENT,
        malloc(sizeof(Card) * INPUT_INCREMENT), 0, INPUT_INCREMENT
    };
    int firstLine = 1, cardRow = 0;
    size_t len;
    char *line;
    int n0, n1, n2, n3, n4;
    Card card;
    while (getline(&line, &len, file) != EOF)
    {
        if (firstLine)
        {
            firstLine = 0;
            char *number = strtok(line, ",");
            while (number != NULL)
            {
                addNumberToInput(&input, atoi(number));
                number = strtok(NULL, ",");
            }
        } else
        {
            cardRow++;
            if (cardRow == 1)
                continue;
            sscanf(line, "%d%*[ ]%d%*[ ]%d%*[ ]%d%*[ ]%d", &n0, &n1, &n2, &n3, &n4);
            card.numbers[cardRow - 2][0] = n0;
            card.numbers[cardRow - 2][1] = n1;
            card.numbers[cardRow - 2][2] = n2;
            card.numbers[cardRow - 2][3] = n3;
            card.numbers[cardRow - 2][4] = n4;
            if (cardRow == 6)
            {
                addCardToInput(&input, card);
                cardRow = 0;
            }
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

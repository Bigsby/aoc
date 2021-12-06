#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <sstream>
#include <algorithm>

using namespace std;

struct Results
{
    int part1;
    int part2;
};

struct Card
{
    bool complete = false;
    int numbers[5][5];
    bool checkComplete(void)
    {
        for (auto x = 0; x < 5; x++)
        {
            auto xComplete = true;
            auto yComplete = true;
            for (auto y = 0; y < 5; y++)
            {
                xComplete &= numbers[x][y] < 0;
                yComplete &= numbers[y][x] < 0;
            }
            if (xComplete || yComplete)
            {
                return complete = true;
            }
        }
        return complete = false;   
    }
};

struct Input
{
    vector<int> numbers;
    vector<Card> cards;
};

int getCardUnmarkedSum(Card card)
{
    auto total = 0;
    for (auto row = 0; row < 5; row++)
        for (auto column = 0; column < 5; column++)
            if (card.numbers[row][column] > 0)
                total += card.numbers[row][column];
    return total;
}

int playGame(const Input input, const bool first)
{
    vector<Card> cards = input.cards;
    for (auto number: input.numbers)
        for (auto &card: cards)
        {
            if (card.complete)
                continue;
            for (auto row = 0; row < 5; row++)
                for (auto column = 0; column < 5; column++)
                    if (card.numbers[row][column] == number)
                    {
                        card.numbers[row][column] = -1;
                        if (card.checkComplete())
                        {
                            if (first)
                                return getCardUnmarkedSum(card) * number;
                            card.complete = true;
                            if (count_if(cards.begin(), cards.end(), [](Card card) { return !card.complete; }) == 0)
                                return getCardUnmarkedSum(card) * number;
                        }
                    }
        }
    throw runtime_error("Game did not finish");
}

Results solve(Input puzzleInput)
{
    return {playGame(puzzleInput, true), playGame(puzzleInput, false)};
}

Input getInput(char *filePath)
{
    ifstream file(filePath);
    if (!file.is_open())
        throw runtime_error("Error reading input file!");

    Input input;
    bool firstLine = true;
    int cardRow = -2;
    string line;
    size_t position;
    Card card;
    while(getline(file, line))
    {
        if (firstLine)
        {
            firstLine = false;
            stringstream numbersLine(line);
            string number;
            while(getline(numbersLine, number, ','))
                input.numbers.push_back(stoi(number));
        } else 
        {
            cardRow++;
            if (cardRow == -1)
                continue;
            stringstream ss(line);
            for (auto index = 0; index < 5; index++)
                ss >> card.numbers[cardRow][index];
            if (cardRow == 4)
            {
                input.cards.push_back(card);
                cardRow = -2;
                card = Card();
            }
        }
    }
    return input;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
        throw runtime_error("Please, add input file path as parameter");

    clock_t begin = clock();
    auto results = solve(getInput(argv[1]));
    clock_t end = clock();
    auto elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    cout << "P1: " << results.part1 << endl;
    cout << "P2: " << results.part2 << endl;
    cout << endl;
    cout.precision(7);
    cout << "Time: " << std::fixed << elapsed_secs << endl;
    return 0;
}

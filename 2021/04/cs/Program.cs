using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    static class Program
    {
        record Card(int[,] numbers);
        record Input(IEnumerable<int> numbers, IEnumerable<Card> cards);
       
        static bool IsCardComplete(Card card)
        {
            for (var row = 0; row < 5; row++)
            {
                var rowComplete = true;
                for (var column = 0; column < 5; column++)
                    rowComplete &= card.numbers[row, column] < 0;
                if (rowComplete)
                    return true;
            }
            for (var column = 0; column < 5; column++)
            {
                var columnComplete = true;
                for (var row = 0; row < 5; row++)
                    columnComplete &= card.numbers[row, column] < 0;
                if (columnComplete)
                    return true;
            }
            return false;
        }

        static int GetCardUnmarkedSum(Card card)
        {
            var total = 0;
            foreach (var number in card.numbers)
                total += number > 0 ? number : 0;
            return total;
        }

        static int PlayGame(Input puzzleInput, bool first)
        {
            var cards = puzzleInput.cards.Select(card => new Card(card.numbers.Clone() as int[,])).ToList();
            foreach (var number in puzzleInput.numbers)
            {
                var toRemove = new List<Card>();
                foreach (var card in cards)
                {
                    for (var row = 0; row < 5; row++)
                        for (var column = 0; column < 5; column++)
                            if (card.numbers[row, column] == number)
                            {
                                card.numbers[row, column] = -100;
                                if (IsCardComplete(card))
                                {
                                    if (first)
                                        return GetCardUnmarkedSum(card) * number;
                                    toRemove.Add(card);
                                }
                            }
                }
                foreach (var card in toRemove)
                {
                    cards.Remove(card);
                    if (!cards.Any())
                        return GetCardUnmarkedSum(card) * number;
                }
            }
            throw new Exception("Game did not finished!");
        }

        static (int, int) Solve(Input puzzleInput)
            => (PlayGame(puzzleInput, true), PlayGame(puzzleInput, false));

        static Input GetInput(string filePath)
        {
            IEnumerable<int> numbers = null;
            var cards = new List<Card>();
            var firstLine = true;
            var cardNumbers = new int[5, 5];
            var cardRow = 0;
            foreach (var line in File.ReadAllLines(filePath))
            {
                if (firstLine)
                {
                    firstLine = false;
                    numbers = line.Split(',').Select(int.Parse);
                } else 
                {
                    cardRow++;
                    if (cardRow == 1)
                        continue;

                    var columnIndex = 0;
                    foreach (var number in line.Split(new [] { ' ' }, StringSplitOptions.RemoveEmptyEntries).Select(int.Parse))
                        cardNumbers[cardRow - 2, columnIndex++] = number;
                    if (cardRow == 6)
                    {
                        cards.Add(new Card(cardNumbers));
                        cardNumbers = new int[5, 5];
                        cardRow = 0;
                    }
                }
            }

            return new Input(numbers, cards);
        }

        static void Main(string[] args)
        {
            if (args.Length != 1) throw new Exception("Please, add input file path as parameter");

            var watch = Stopwatch.StartNew();
            var (part1Result, part2Result) = Solve(GetInput(args[0]));
            watch.Stop();
            WriteLine($"P1: {part1Result}");
            WriteLine($"P2: {part2Result}");
            WriteLine();
            WriteLine($"Time: {(double)watch.ElapsedTicks / 100 / TimeSpan.TicksPerSecond:f7}");
        }
    }
}

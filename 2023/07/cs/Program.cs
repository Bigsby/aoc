using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<Tuple<string,int>>;

    enum HandType {
        HighCard = 0,
        OnePair  = 1,
        TwoPair  = 2,
        ThreeOfAKind = 3,
        FullHouse = 4,
        FourOfAKind = 5,
        FiveOfAKind = 6
    }

    static class Program
    {
        const char JOKER = 'J';
        static char[] PART1_CARD_ORDER = new [] { '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'};
        static char[] PART2_CARD_ORDER = new [] { JOKER, '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'};
        static HandType GetHandType(string hand, bool useJoker = false)
        {
            var distinctCards = hand.Distinct().ToDictionary(card => card, card => hand.Count(c => c == card));
            if (distinctCards.Count > 1 && useJoker && distinctCards.ContainsKey(JOKER))
            {
                distinctCards[distinctCards.Where(pair => pair.Key != JOKER).MaxBy(pair => pair.Value).Key] += distinctCards[JOKER];
                distinctCards.Remove(JOKER);
            }
            
            return distinctCards.Count switch {
                4 => HandType.OnePair,
                3 => distinctCards.Values.Any(count => count == 3) ? HandType.ThreeOfAKind : HandType.TwoPair,
                2 => distinctCards.Values.Any(count => count == 4) ? HandType.FourOfAKind : HandType.FullHouse,
                1 => HandType.FiveOfAKind,
                _ => HandType.HighCard
            };
        }

        class HandComparer : IComparer<string>
        {
            private readonly char[] _order;
            public HandComparer(char[] order) => _order = order;

            public int Compare(string a, string b)
            {
                for (var index = 0; index < a.Length; index++)
                    if (a[index] == b[index])
                        continue;
                    else
                        return Array.IndexOf(_order, a[index]).CompareTo(Array.IndexOf(_order, b[index]));
                return 0;
            }
        }

        static int GetTotalWinnings(Input puzzleInput, char[] cardsOrder, bool useJoker)
        {
            var handComparer = new HandComparer(cardsOrder);
            var ordered = puzzleInput.OrderBy<Tuple<string,int>,int>(hand => (int)GetHandType(hand.Item1, useJoker)).ThenBy(hand => hand.Item1, handComparer);
            var rank = 1;
            var winnings = 0;
            foreach (var (_, bid) in ordered)
                winnings += bid * rank++;
            return winnings;
        }

        static (int, int) Solve(Input puzzleInput)
            => (GetTotalWinnings(puzzleInput, PART1_CARD_ORDER, false), GetTotalWinnings(puzzleInput, PART2_CARD_ORDER, true));

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line =>
            {
                var split = line.Trim().Split(' ');
                return Tuple.Create(split[0], int.Parse(split[1]));
            });

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

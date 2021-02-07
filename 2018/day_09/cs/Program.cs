using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class Marble
    {
        public Marble(int number, Marble previous, Marble next)
        {
            Number = number;
            Previous = previous ?? this;
            Previous.Next = this;
            Next = next ?? this;
            Next.Previous = this;
        }
        public int Number { get; init; }
        public Marble Previous { get; set; }
        public Marble Next { get; set; }
    }

    class Cycle<T>
    {
        private IEnumerator<T> _enumerator;
        public Cycle(IEnumerable<T> source) => _enumerator = source.GetEnumerator();
        public T Next()
        {
            if (!_enumerator.MoveNext())
            {
                _enumerator.Reset();
                _enumerator.MoveNext();
            }
            return _enumerator.Current;
        }
    }

    class Program
    {
        static long PlayGame(int playerCount, int lastMarble)
        {
            var scores = Enumerable.Range(0, playerCount).ToDictionary(index => index + 1, _ => 0L);
            var players = new Cycle<int>(scores.Keys);
            var currentPlayer = players.Next();
            var currentMarble = new Marble(0, null, null);
            var nextNumber = 0;
            while (nextNumber <= lastMarble)
            {
                nextNumber++;
                currentPlayer = players.Next();
                if (nextNumber % 23 != 0)
                    currentMarble = new Marble(nextNumber, currentMarble.Next, currentMarble.Next.Next);
                else
                {
                    foreach (var _ in Enumerable.Range(0, 6))
                        currentMarble = currentMarble.Previous;
                    var marbleToRemove = currentMarble.Previous;
                    scores[currentPlayer] += nextNumber + marbleToRemove.Number;
                    marbleToRemove.Previous.Next = currentMarble;
                    currentMarble.Previous = marbleToRemove.Previous;
                }
            }
            return scores.Values.Max();
        }

        static long Part1(Tuple<int, int> puzzleInput) => PlayGame(puzzleInput.Item1, puzzleInput.Item2);

        static long Part2(Tuple<int, int> puzzleInput) => PlayGame(puzzleInput.Item1, puzzleInput.Item2 * 100);

        static Regex inputRegex = new Regex(@"^(?<players>\d+) players; last marble is worth (?<last>\d+)");
        static Tuple<int, int> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var match = inputRegex.Match(File.ReadAllText(filePath));
            if (match.Success)
                return Tuple.Create(int.Parse(match.Groups["players"].Value), int.Parse(match.Groups["last"].Value));
            throw new Exception("Bad input");
        }

        static void Main(string[] args)
        {
            if (args.Length != 1) throw new Exception("Please, add input file path as parameter");

            var puzzleInput = GetInput(args[0]);
            var watch = Stopwatch.StartNew();
            var part1Result = Part1(puzzleInput);
            watch.Stop();
            var middle = watch.ElapsedTicks;
            watch = Stopwatch.StartNew();
            var part2Result = Part2(puzzleInput);
            watch.Stop();
            WriteLine($"P1: {part1Result}");
            WriteLine($"P2: {part2Result}");
            WriteLine();
            WriteLine($"P1 time: {(double)middle / 100 / TimeSpan.TicksPerSecond:f7}");
            WriteLine($"P2 time: {(double)watch.ElapsedTicks / 100 / TimeSpan.TicksPerSecond:f7}");
        }
    }
}
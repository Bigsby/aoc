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
        static (long, long) Solve(Tuple<int, int> puzzleInput)
        {
            var (playerCount, lastMarble) = puzzleInput;
            var scores = Enumerable.Range(0, playerCount).ToDictionary(index => index + 1, _ => 0L);
            var players = new Cycle<int>(scores.Keys);
            var currentPlayer = players.Next();
            var currentMarble = new Marble(0, null, null);
            var nextNumber = 0;
            var part1Result = 0L;
            while (nextNumber <= lastMarble * 100)
            {
                nextNumber++;
                if (nextNumber == lastMarble)
                    part1Result = scores.Values.Max();
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
            return (part1Result, scores.Values.Max());
        }

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
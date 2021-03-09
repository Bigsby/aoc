using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        static (long, long) Solve(Tuple<int, int> puzzleInput)
        {
            var (elvesCount, lastMarble) = puzzleInput;
            var scores = new long[elvesCount];
            var circle = new LinkedList<int>();
            var current_marble = circle.AddFirst(0);
            var part1Score = 0L;
            for (var nextMarble = 1; nextMarble <= lastMarble * 100; nextMarble++)
            {
                if (nextMarble == lastMarble)
                    part1Score = scores.Max();
                if (nextMarble % 23 == 0)
                {
                    for (var rotate = 0; rotate < 7; rotate++)
                        current_marble = current_marble.Previous ?? circle.Last;
                    scores[nextMarble % elvesCount] += nextMarble + current_marble.Value;
                    var toRemove = current_marble;
                    current_marble = current_marble.Next ?? circle.First;
                    circle.Remove(toRemove);
                }
                else
                {
                    current_marble = current_marble.Next ?? circle.First;
                    current_marble = circle.AddAfter(current_marble, nextMarble);
                }
            }
            return (part1Score, scores.Max());
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
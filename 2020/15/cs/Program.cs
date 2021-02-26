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
        static (int, int) Solve(IEnumerable<int> numbers)
        {
            var part1Result = 0;
            var turn = 0;
            var occurrences = new Dictionary<int, (int lastOccurrence, int secondLastOccurence)>();
            foreach (var number in numbers)
                occurrences[number] = (++turn, 0);
            var lastNumber = numbers.Last();
            while (turn < 30_000_000)
            {
                if (turn == 2020)
                    part1Result = lastNumber;
                turn++;
                var (lastOccurrence, secondLastOccurence) = occurrences[lastNumber];
                if (secondLastOccurence == 0)
                    lastNumber = 0;
                else
                    lastNumber = lastOccurrence - secondLastOccurence;
                if (occurrences.ContainsKey(lastNumber))
                    occurrences[lastNumber] = (turn, occurrences[lastNumber].lastOccurrence);
                else
                    occurrences[lastNumber] = (turn, 0);
            }
            return (part1Result, lastNumber);
        }

        static IEnumerable<int> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Split(',').Select(int.Parse);

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
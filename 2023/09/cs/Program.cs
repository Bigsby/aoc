using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<IEnumerable<int>>;

    static class Program
    {
        static int GetNextValue(IEnumerable<int> history, bool last = true)
        {
            var current = history;
            var edgeNumbers = new List<int>();
            while (current.Any(number => number != 0))
            {
                edgeNumbers.Add(last ? current.Last() : current.First());
                current = Enumerable.Range(0, current.Count() - 1).Select(index => current.ElementAt(index + 1) - current.ElementAt(index)).ToArray();
            }
            if (last)
                return edgeNumbers.Sum();
            edgeNumbers.Reverse();
            return edgeNumbers.Aggregate(0, (soFar, next) => next - soFar);
        }

        static int Part1(Input puzzleInput)
        { 
            return puzzleInput.Sum(history => GetNextValue(history));
        }

        static int Part2(Input puzzleInput)
        {
            return puzzleInput.Sum(history => GetNextValue(history, false));
        }

        static (int, int) Solve(Input puzzleInput)
            => (puzzleInput.Sum(history => GetNextValue(history)), puzzleInput.Sum(history => GetNextValue(history, false)));

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => line.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries).Select(int.Parse));

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

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
        static int Part1(IEnumerable<int> crabs)
        { 
            crabs = crabs.OrderBy(position => position);
            var mean = crabs.ElementAt((int)(crabs.Count() / 2));
            return crabs.Sum(position => Math.Abs(mean - position));
        }

        static int GetDistanceCost(int posA, int posB)
        {
            int distance = Math.Abs(posA - posB);
            return (distance * (distance + 1)) / 2;
        }

        static int Part2(IEnumerable<int> crabs)
        {
            int average = (int)(crabs.Sum() / crabs.Count());
            return crabs.Sum(position => GetDistanceCost(average, position));
        }

        static (int, int) Solve(IEnumerable<int> puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static IEnumerable<int> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim().Split(',').Select(int.Parse);

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

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
        static int Part1(IEnumerable<int> depths)
        { 
            var increments = 0;
            var lastDepth = int.MaxValue;
            foreach (var depth in depths)
            {
                if (depth > lastDepth)
                    increments++;
                lastDepth = depth;
            }
            return increments;
        }

        static int Part2(IEnumerable<int> depths)
        {
            var increments = 0;
            var lastDepth = int.MaxValue;
            for (var index = 0; index < depths.Count() - 2; index++)
            {
                var depth = depths.Skip(index).Take(3).Sum();
                if (depth > lastDepth)
                    increments++;
                lastDepth = depth;
            }
            return increments;
        }

        static (int, int) Solve(IEnumerable<int> puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static IEnumerable<int> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(int.Parse);

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

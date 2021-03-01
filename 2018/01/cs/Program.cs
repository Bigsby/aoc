using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    class Program
    {
        static int Part2(int[] changes)
        {
            var changesLength = changes.Count();
            var frequency = 0;
            var previous = new HashSet<int>();
            var index = 0;
            while (previous.Add(frequency))
            {
                frequency += changes[index];
                index = (index + 1) % changesLength;
            }
            return frequency;
        }

        static (int, int) Solve(int[] changes)
            => (
                changes.Sum(),
                Part2(changes)
            );

        static int[] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(int.Parse).ToArray();

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
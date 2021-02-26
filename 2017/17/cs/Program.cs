using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;

namespace AoC
{
    static class Program
    {
        static int Part1(int steps)
        { 
            var spinlock = new List<int> { 0 };
            var position = 0;
            for (var number = 1; number <= 2017; number++)
            {
                position = (position + steps) % spinlock.Count + 1;
                spinlock.Insert(position, number);
            }
            return spinlock[position + 1];
        }

        static int Part2(int steps)
        {
            var position = 0;
            var result = 0;
            for (var number = 1; number <= 50_000_000; number++)
            {
                position = ((position + steps) % number) + 1;
                if (position == 1)
                    result = number;
            }
            return result;
        }

        static (int, int) Solve(int steps)
            => (
                Part1(steps),
                Part2(steps)
            );

        static int GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : int.Parse(File.ReadAllText(filePath).Trim());

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

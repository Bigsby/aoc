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

        static int GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return int.Parse(File.ReadAllText(filePath).Trim());
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

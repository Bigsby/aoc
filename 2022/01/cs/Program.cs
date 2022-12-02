using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Elf = List<int>;
    static class Program
    {
        static (int, int) Solve(List<Elf> elves)
        {
            int[] topElves = new[] { 0, 0, 0 };
            foreach (var elf in elves)
            {
                var elfSum = elf.Sum();
                foreach (var index in Enumerable.Range(0, 3))
                {
                    if (elfSum > topElves[index])
                    {
                        var temp = topElves[index];
                        topElves[index] = elfSum;
                        elfSum = temp;
                    }
                }
            }
            return (topElves[0], topElves.Sum());
        }

        static List<Elf> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);

            var elves = new List<Elf>();
            var currentElf = new Elf();
            foreach (var line in File.ReadAllLines(filePath))
                if (string.IsNullOrEmpty(line))
                {
                    elves.Add(currentElf);
                    currentElf = new Elf();
                }
                else
                    currentElf.Add(int.Parse(line));
            elves.Add(currentElf);
            return elves;
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

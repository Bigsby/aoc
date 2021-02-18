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
        static long Part1(IEnumerable<(long lower, long upper)> ranges)
        {
            ranges = ranges.OrderBy(range => range.lower);
            var previousUpper = 0L;
            foreach (var (lower, upper) in ranges)
            {
                if (upper <= previousUpper)
                    continue;
                if (lower <= previousUpper + 1)
                    previousUpper = upper;
                else
                    return previousUpper + 1;
            }
            throw new Exception("IP not found");
        }

        static long Part2(IEnumerable<(long lower, long upper)> ranges)
        {
            ranges = ranges.OrderBy(range => range.lower);
            var previousUpper = 0L;
            var allowedCount = 0L;
            foreach (var (lower, upper) in ranges)
            {
                if (upper <= previousUpper)
                    continue;
                if (lower > previousUpper + 1)
                    allowedCount += lower - previousUpper - 1;
                previousUpper = upper;
            }
            return allowedCount;
        }

        static IEnumerable<(long, long)> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line => {
                var splits = line.Trim().Split('-');
                return (long.Parse(splits[0]), long.Parse(splits[1]));
            });
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

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
        static (long, long) Solve(IEnumerable<(long lower, long upper)> ranges)
        {
            ranges = ranges.OrderBy(range => range.lower);
            var previousUpper = 0L;
            var allowedCount = 0L;
            var part1Result = 0L;
            foreach (var (lower, upper) in ranges)
            {
                if (upper <= previousUpper)
                    continue;
                if (lower > previousUpper + 1)
                {
                    allowedCount += lower - previousUpper - 1;
                    if (part1Result == 0)
                        part1Result = previousUpper + 1;
                }
                previousUpper = upper;
            }
            return (part1Result, allowedCount);
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

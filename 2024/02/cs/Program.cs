using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<int[]>;

    static class Program
    {
        static bool IsReportSafe(int[] report)
        {
            var increasing = report.First() < report.Last();
            var minimumInterval = increasing ? -3 : 1;
            var maximumInterval = increasing ? -1 : 3;
            for (var index = 0; index < report.Length - 1; index++)
            {
                var difference = report[index] - report[index + 1];
                if(difference == 0
                    ||
                    difference < minimumInterval
                    ||
                    difference > maximumInterval)
                    return false;
            }
            return true;
        }

        static bool IsReportSafe(int[] report, bool useSkip)
        {
            var isSafe = IsReportSafe(report);
            if (!isSafe && useSkip)
                for (var indexToRemove = 0; indexToRemove < report.Length; indexToRemove++)
                    if (IsReportSafe(report.Where((_, index) => index != indexToRemove).ToArray()))
                        return true;
            return isSafe;
        }

        static (int, int) Solve(Input puzzleInput)
            => (puzzleInput.Count(report => IsReportSafe(report, false)), puzzleInput.Count(report => IsReportSafe(report, true)));

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? 
            throw new FileNotFoundException(filePath)
            :
            File.ReadAllLines(filePath).Select(line => line.Trim().Split().Select(int.Parse).ToArray());

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

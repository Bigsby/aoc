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
        static long RunGenerations(IEnumerable<int> fishes, int generations)
        {
            var fishCounts = new long[9];
            foreach (var fish in fishes)
                fishCounts[fish]++;
            while (generations-- > 0)
            {
                long fishesAtZero = fishCounts[0];
                for (int day = 0; day < 8; day++)
                    fishCounts[day] = fishCounts[day + 1];
                fishCounts[8] = fishesAtZero;
                fishCounts[6] += fishesAtZero;
            }
            return fishCounts.Sum();
        }

        static (long, long) Solve(IEnumerable<int> puzzleInput)
            => (RunGenerations(puzzleInput, 80), RunGenerations(puzzleInput, 256));

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

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
        static long[] DIVISORS = new[] { 2L, 3, 5, 7, 11, 13 };
        static long CalculatePowers(long[] powers) =>
            (long)powers.Zip(DIVISORS, (k, j) => Math.Pow(j, k))
                .Aggregate(1.0, (acc, v) => acc * (double)v);

        static IEnumerable<long[]> GetPowers(long[] limits)
        {
            var powers = new long[6];
            yield return powers;
            while (true)
            {
                bool all_equal = true;
                for (var index = 0; index < 6; index++)
                    all_equal &= powers[index] == limits[index];
                if (all_equal)
                    yield break;
                for (var index = 5; index >= 0; index--)
                    if (powers[index] < limits[index])
                    {
                        powers[index]++;
                        for (var overflow = index + 1; overflow < 6; overflow++)
                            powers[overflow] = 0;
                        break;
                    }
                yield return powers;
            }
        }

        static long[] MAX_POWERS = new[] { 6L, 4, 2, 2, 2, 2 };
        static long GetHouse(long target, long multiplier, long limit)
        {
            var minimumHouse = long.MaxValue;
            foreach (var housePowers in GetPowers(MAX_POWERS))
            {
                var house = CalculatePowers(housePowers);
                var housePresents = 0L;
                foreach (var elfPowers in GetPowers(housePowers))
                {
                    var elfPresents = CalculatePowers(elfPowers);
                    if (house / elfPresents <= limit)
                        housePresents += elfPresents;
                }
                if (housePresents * multiplier >= target && house < minimumHouse)
                    minimumHouse = house;
            }
            return minimumHouse;
        }

        static (long, long) Solve(long puzzleInput)
        {
            return (
                GetHouse(puzzleInput, 10, int.MaxValue),
                GetHouse(puzzleInput, 11, 50)
            );
        }

        static long GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : long.Parse(File.ReadAllText(filePath));

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

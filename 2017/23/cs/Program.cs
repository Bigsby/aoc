using System;
using static System.Console;
using System.IO;
using System.Diagnostics;

namespace AoC
{
    static class Program
    {
        static int Part1(int number)
            => (int)Math.Pow(number - 2, 2);

        static int Part2(int number)
        {
            var total = number * 100 + 100_000;
            var nonPrimes = 0;
            for (var candidate = total; candidate < total + 17000 + 1; candidate += 17)
            {
                var divider = 2;
                while (candidate % divider != 0)
                    divider += 1;
                if (candidate != divider)
                    nonPrimes++;
            }
            return nonPrimes;
        }

        static (int, int) Solve(int number)
            => (
                (int)Math.Pow(number - 2, 2),
                Part2(number)
            );

        static int GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : int.Parse(File.ReadAllLines(filePath)[0].Trim().Split(" ")[2]);

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

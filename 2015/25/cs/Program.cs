using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Text.RegularExpressions;

namespace AoC
{
    static class Program
    {
        const long FIRST_CODE = 20151125;
        const long MULTIPLIER = 252533;
        const long DIVIDER = 33554393;
        static (long, object) Solve((int, int) data)
        {
            var (targetRow, targetColumn) = data;
            var lastCode = FIRST_CODE;
            var currentLength = 1;
            while (true)
            {
                var column = 0;
                var row = ++currentLength;
                while (row > 0)
                {
                    column++;
                    lastCode = (lastCode * MULTIPLIER) % DIVIDER;
                    if (column == targetColumn && row == targetRow)
                        return (lastCode, null);
                    row--;
                }
            }
        }

        static (int, int) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var matches = Regex.Matches(File.ReadAllText(filePath), @"\d+");
            return (int.Parse(matches[0].Value), int.Parse(matches[1].Value));
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

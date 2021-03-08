using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        static Regex hexaRegex = new Regex(@"\\x[0-9a-f]{2}", RegexOptions.Compiled);
        static int GetStringDifference1(string str)
        {
            var initialLength = str.Length;
            var stripped = str.Replace(@"\\", "r")
                .Replace("\\\"", "r");
            stripped = hexaRegex.Replace(stripped, "r");
            return initialLength - stripped.Trim('"').Length;
        }

        static int GetStringDifference2(string str)
            => 2 + Regex.Escape(str).Replace("\"", "\\\"").Length - str.Length;

        static (int, int) Solve(IEnumerable<string> strings)
            => (
                strings.Sum(GetStringDifference1),
                strings.Sum(GetStringDifference2)
            );

        static IEnumerable<string> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => line.Trim());

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
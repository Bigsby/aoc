using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Net;

namespace AoC
{
    using Input = IEnumerable<string>;

    static class Program
    {
        static Dictionary<string, int> VALUES = new Dictionary<string, int>{
            { "1", 1 },
            { "2", 2 },
            { "3", 3 },
            { "4", 4 },
            { "5", 5 },
            { "6", 6 },
            { "7", 7 },
            { "8", 8 },
            { "9", 9 }
        };

        static Dictionary<string, int> ALPHA_VALUES = new Dictionary<string, int> {
            { "one", 1 },
            { "two", 2 },
            { "three", 3 },
            { "four", 4 },
            { "five", 5 },
            { "six", 6 },
            { "seven", 7 },
            { "eight", 8 },
            { "nine", 9 }
        }.Concat(VALUES).ToDictionary(pair => pair.Key, pair => pair.Value);

        static int GetValue(string line, IDictionary<string, int> values, int multiplier, Func<int,Index> rangeFunc)
        {
            foreach (var index in Enumerable.Range(0, line.Length))
            {
                var key = values.Keys.FirstOrDefault(key => line[rangeFunc(index)..].StartsWith(key));
                if (!string.IsNullOrEmpty(key))
                    return values[key] * multiplier;
            }
            throw new Exception($"Value not found in {line}");
        }


        static int GetSum(Input puzzleInput, IDictionary<string, int> values)
            => puzzleInput.Sum(line => GetValue(line, values, 10, index => index) + GetValue(line, values, 1, index => ^(index + 1)));

        static (int, int) Solve(Input puzzleInput)
            => (GetSum(puzzleInput, VALUES), GetSum(puzzleInput, ALPHA_VALUES));

        static Input GetInput(string filePath)
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

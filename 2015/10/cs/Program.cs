using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Text.RegularExpressions;
using System.Text;

namespace AoC
{
    class Program
    {
        static Regex testRegex = new Regex(@"(\d)\1+|\d", RegexOptions.Compiled);
        static string GetNextValue(string value)
        {
            var sequeces = new StringBuilder();
            foreach (Match match in testRegex.Matches(value))
            {
                var group = match.Groups[0].Value;
                sequeces.Append(group.Length);
                sequeces.Append(group[0]);
            }
            return sequeces.ToString();
        }

        static (int, int) Solve(string puzzleInput)
        {
            var currentValue = puzzleInput;
            var part1 = 0;
            for (var turn = 0; turn < 50; turn++)
            {
                if (turn == 40)
                    part1 = currentValue.Length;
                currentValue = GetNextValue(currentValue);
            }
            return (part1, currentValue.Length);
        }
            
        static string GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath) 
            : File.ReadAllText(filePath);

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
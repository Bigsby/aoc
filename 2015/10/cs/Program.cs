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
        static Regex testRegex = new Regex(@"(\d)\1+|\d", RegexOptions.Compiled);
        static string GetNextValue(string value)
        {
            var sequeces = new List<string>();
            foreach (Match match in testRegex.Matches(value))
            {
                var group = match.Groups[0].Value;
                sequeces.Add(group.Length.ToString());
                sequeces.Add(group[0].ToString());
            }
            return string.Join("", sequeces);
        }

        static int RunLookAndSay(string puzzleInput, int turns)
            => Enumerable.Range(0, turns)
                .Aggregate(puzzleInput, (currentValue, _) => GetNextValue(currentValue)).Length;

        static int Part1(string puzzleInput) => RunLookAndSay(puzzleInput, 40);

        static int Part2(string puzzleInput) => RunLookAndSay(puzzleInput, 50);

        static string GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath);
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
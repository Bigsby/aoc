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
        static string[] FORBIDEN_PAIRS = new[] { "ab", "cd", "pq", "xy" };
        static Regex vowelRegex = new Regex(@"[aeiou]", RegexOptions.Compiled);
        static Regex repeatRegex = new Regex(@"(.)\1{1,}", RegexOptions.Compiled);
        static int Part1(IEnumerable<string> words) => words.Count(word =>
            FORBIDEN_PAIRS.All(pair => !word.Contains(pair))
            && vowelRegex.Matches(word).Count > 2 
            && repeatRegex.Matches(word).Count != 0
        );

        static bool HasRepeatingPair(string word)
            =>  Enumerable.Range(0, word.Length - 2).Any(pairStart => {
                var pairToTest = word[new Range(pairStart, pairStart + 2)];
                return word[Range.EndAt(pairStart)].Contains(pairToTest) 
                    || word[Range.StartAt(pairStart + 2)].Contains(pairToTest);
            });

        static bool HasRepeatingLetter(string word)
            => Enumerable.Range(0, word.Length - 2).Any(index => word[index] == word[index + 2]);

        static int Part2(IEnumerable<string> words)
            => words.Count(word => HasRepeatingPair(word) && HasRepeatingLetter(word));

        static IEnumerable<string> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(line => line.Trim());
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
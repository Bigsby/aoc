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
            !FORBIDEN_PAIRS.Any(pair => word.Contains(pair))
            && vowelRegex.Matches(word).Count > 2 
            && repeatRegex.IsMatch(word)
        );

        static bool HasRepeatingPair(string word)
            =>  Enumerable.Range(0, word.Length - 2).Any(pairStart => {
                var pairToTest = word[new Range(pairStart, pairStart + 2)];
                return word[Range.StartAt(pairStart + 2)].Contains(pairToTest);
            });

        static bool HasRepeatingLetter(string word)
            => Enumerable.Range(0, word.Length - 2).Any(index => word[index] == word[index + 2]);

        static (int, int) Solve(IEnumerable<string> words)
            => (Part1(words), words.Count(word => HasRepeatingPair(word) && HasRepeatingLetter(word)));

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
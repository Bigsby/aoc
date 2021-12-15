using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = Tuple<string, Dictionary<string, string>>;
    static class Program
    {
        static void AddToCounts(IDictionary<string, ulong> counts, string pair, ulong count)
        {
            if (counts.ContainsKey(pair))
                counts[pair] += count;
            else
                counts[pair] = count;
        }

        static ulong CountInsertions(Input puzzleInput, int steps)
        {
            var (polymer, rules) = puzzleInput;
            var pairOccurences = new Dictionary<string, ulong>();
            for (var index = 0; index < polymer.Length - 1; index++)
                AddToCounts(pairOccurences, polymer.Substring(index, 2), 1);
            while (steps-- > 0)
            {
                var newPairOccurences = new Dictionary<string, ulong>();
                foreach (var (pair, occurences) in pairOccurences)
                {
                    var first = pair[0];
                    var second = pair[1];
                    var newLetter = rules[pair];
                    AddToCounts(newPairOccurences, first + newLetter, occurences);
                    AddToCounts(newPairOccurences, newLetter + second, occurences);
                }
                pairOccurences = newPairOccurences;
            }
            var letterOccurences = new Dictionary<string, ulong>();
            foreach (var (pair, occurences) in pairOccurences)
                AddToCounts(letterOccurences, pair.Substring(1, 1), occurences);
            return letterOccurences.Values.Max() - letterOccurences.Values.Min();
        }

        static (ulong, ulong) Solve(Input puzzleInput)
            => (CountInsertions(puzzleInput, 10), CountInsertions(puzzleInput, 40));

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            string polymer = "";
            var rules = new Dictionary<string, string>();
            foreach (var line in File.ReadAllLines(filePath))
            {
                if (string.IsNullOrEmpty(polymer))
                    polymer = line;
                else if (!string.IsNullOrEmpty(line))
                {
                    var split = line.Split(" -> ");
                    rules[split[0]] = split[1];
                }
            }
            return Tuple.Create(polymer, rules);
            //: File.ReadAllText(filePath).Trim();
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

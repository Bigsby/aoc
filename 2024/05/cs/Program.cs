using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    record struct Rule(int Before, int After);
    record struct Input(Rule[] Rules, int[][] Updates);

    static class Program
    {
        static bool IsUpdateCorrect(int[] update, Rule[] rules)
        {
            for (var index = 1; index < update.Length; index++)
                foreach (var previousPage in  update.Take(index))
                    if (rules.Any(rule => rule.Before == update[index] && rule.After == previousPage))
                        return false;
            return true;
        }

        static int Part1(Input puzzleInput)
            => puzzleInput.Updates
                .Where(update => IsUpdateCorrect(update, puzzleInput.Rules))
                .Sum(update => update[update.Length / 2]);

        static int OrderUpdateAndGetMiddle(int[] update, Rule[] rules)
        {
            var orderedUpdate = new List<int>();
            foreach (var page in update)
            {
                var insertIndex = 0;
                for (insertIndex = 0; insertIndex < orderedUpdate.Count; insertIndex++)
                    if (rules.Any(rule => rule.Before == page && rule.After == orderedUpdate[insertIndex]))
                        break;
                orderedUpdate.Insert(insertIndex, page);
            }
            return orderedUpdate[update.Length / 2];
        }

        static int Part2(Input puzzleInput)
            => puzzleInput.Updates
                .Where(update => !IsUpdateCorrect(update, puzzleInput.Rules))
                .Sum(update => OrderUpdateAndGetMiddle(update, puzzleInput.Rules));

        static (int, int) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) 
                throw new FileNotFoundException(filePath);

            var rules = new List<Rule>();
            var updates = new List<int[]>();

            var readingRules = true;
            foreach (var line in File.ReadAllLines(filePath))
            {
                if (string.IsNullOrEmpty(line))
                {
                    readingRules = false;
                    continue;
                }

                if (readingRules)
                {
                    var split = line.Split('|');
                    rules.Add(new (int.Parse(split[0]), int.Parse(split[1])));
                }
                else
                    updates.Add(line.Split(',').Select(int.Parse).ToArray());
            }

            return new(rules.ToArray(), updates.ToArray());
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

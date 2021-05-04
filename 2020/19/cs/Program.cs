using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Rules = Dictionary<int, Rule>;

    record Rule();

    record LetterRule : Rule
    {
        public char letter { get; init; }
        public LetterRule(string letter)
            => this.letter = letter[0];
    }

    record SetRule : Rule
    {
        public IEnumerable<IEnumerable<int>> sets { get; init; }
        public SetRule(string definition)
            => sets = definition.Split("|").Select(set => set.Trim().Split(" ").Select(int.Parse).ToArray());
    }

    static class Program
    {
        static IEnumerable<int> FindMatchedIndexes(Rules rules, string message, int ruleNumber = 0, int index = 0)
        {
            if (index == message.Length)
                return new int[0];
            var rule = rules[ruleNumber];
            if (rule is LetterRule letterRule)
            {
                if (message[index] == letterRule.letter)
                    return new[] { index + 1 };
                return new int[0];
            }
            var matches = new List<int>();
            var setRule = rule as SetRule;
            foreach (var ruleSet in setRule.sets)
            {
                var subMatches = new List<int>(new[] { index });
                foreach (var subRule in ruleSet)
                {
                    var newMatches = new List<int>();
                    foreach (var sub_match_index in subMatches)
                        newMatches.AddRange(FindMatchedIndexes(rules, message, subRule, sub_match_index));
                    subMatches = newMatches;
                }
                matches.AddRange(subMatches);
            }
            return matches;
        }

        static (int, int) Solve((Rules, List<string>) puzzleInput)
        {
            var (rules, messages) = puzzleInput;
            var part1Result = messages.Count(message => FindMatchedIndexes(rules, message).Contains(message.Length));
            rules[8] = new SetRule("42 | 42 8");
            rules[11] = new SetRule("42 31 | 42 11 31");
            return (
                part1Result,
                messages.Count(message => FindMatchedIndexes(rules, message).Contains(message.Length))
            );
        }

        static Regex letterRegex = new Regex("^\\\"(?<letter>a|b)\\\"$", RegexOptions.Compiled);
        static Regex ruleRegex = new Regex(@"(?<number>^\d+):\s(?<rule>.+)$", RegexOptions.Compiled);
        static (Rules, List<string>) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var rules = new Rules();
            var messages = new List<string>();
            foreach (var line in File.ReadLines(filePath))
            {
                if (!string.IsNullOrEmpty(line.Trim()))
                {
                    var ruleMatch = ruleRegex.Match(line);
                    if (ruleMatch.Success)
                    {
                        try
                        {
                            var ruleNumber = ruleMatch.Groups["number"].Value;
                            var definition = ruleMatch.Groups["rule"].Value.Trim();
                            var letterMatch = letterRegex.Match(definition);
                            rules[int.Parse(ruleNumber)] = letterMatch.Success ?
                                new LetterRule(letterMatch.Groups["letter"].Value)
                                :
                                new SetRule(definition);
                        }
                        catch
                        {
                            WriteLine(line);
                            ReadLine();
                        }
                    }
                    messages.Add(line.Trim());
                }
            }
            return (rules, messages);
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

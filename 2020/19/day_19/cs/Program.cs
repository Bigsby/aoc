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

    record Rule(string number);

    record LetterRule : Rule
    {
        public string letter { get; init; }
        public LetterRule(string number, string letter) : base(number)
            => this.letter = letter;
    }

    record SetRule : Rule
    {
        public IEnumerable<IEnumerable<int>> sets { get; init; }
        public SetRule(string number, string definition) : base(number)
            => sets = definition.Split("|").Select(set => set.Trim().Split(" ").Select(int.Parse).ToArray());
    }

    static class Program
    {
        static string GenerateRegex(Rules rules, int ruleNumber)
        {
            var rule = rules[ruleNumber];
            return rule switch
            {
                LetterRule letterRule => letterRule.letter,
                SetRule setRule => "(?:" + 
                    string.Join("|", 
                        setRule.sets.Select(ruleSet => string.Join("", ruleSet.Select(innerRule => GenerateRegex(rules, innerRule))))                        
                    ) + ")",
                _ => throw new Exception("Unrecoginzed rule")
            };
        }

        static int Part1((Rules, List<string>) puzzleInput)
        {
            var (rules, messages) = puzzleInput;
            var zeroRule = "^" +  GenerateRegex(rules, 0) + "$";
            return messages.Count(message => Regex.IsMatch(message, zeroRule));
        }

        static (bool, int) isInnerMatch(string rule, string message, int position)
        {
            var match = Regex.Match(message[Range.StartAt(position)], rule);
            if (match.Success)
                return (true, position + match.Index + match.Length);
            return (false, position);
        }

        static bool IsMatch(string firstRule, string secondRule, string message)
        {
            var count = 0;
            var (matched, position) = isInnerMatch(firstRule, message, 0);
            while (matched && position < message.Length)
            {
                var lastPosition = position;
                foreach (var _ in Enumerable.Range(0, count))
                {
                    (matched, position) = isInnerMatch(secondRule, message, position);
                    if (!matched)
                    {
                        position = lastPosition;
                        break;
                    }
                    else if (position == message.Length)
                        return true;
                }
                count++;
                (matched, position) = isInnerMatch(firstRule, message, position);
            }
            return false;
        }

        static int Part2((Rules, List<string>) puzzleInput)
        {
            var (rules, messages) = puzzleInput;
            var rule42 = "^" + GenerateRegex(rules, 42);
            var rule31 = "^" + GenerateRegex(rules, 31);
            return messages.Count(message => IsMatch(rule42, rule31, message));
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
                        try {
                        var ruleNumber = ruleMatch.Groups["number"].Value;
                        var definition = ruleMatch.Groups["rule"].Value.Trim();
                        var letterMatch = letterRegex.Match(definition);
                        rules[int.Parse(ruleNumber)] = letterMatch.Success ?
                            new LetterRule(ruleNumber, letterMatch.Groups["letter"].Value)
                            :
                            new SetRule(ruleNumber, definition);
                        }
                        catch {
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

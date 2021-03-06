﻿using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Rules = IDictionary<string, IEnumerable<(string color, int quantity)>>;

    class Program
    {
        const string REQUIRED_COLOR = "shiny gold";

        static IEnumerable<string> GetRulesContaining(string color, Rules rules)
        {
            foreach (var rule in rules)
                if (rule.Value.Any(innerRule => innerRule.color == color))
                {
                    yield return rule.Key;
                    foreach (var innerColor in GetRulesContaining(rule.Key, rules))
                        yield return innerColor;
                }
        }

        static int GetQuantityFromColor(string color, Rules rules)
            => rules[color].Sum(innerRule => innerRule.quantity * ( 1 + GetQuantityFromColor(innerRule.color, rules)));

        static (int, int) Solve(Rules rules)
            => (
                GetRulesContaining(REQUIRED_COLOR, rules).Distinct().Count(),
                GetQuantityFromColor(REQUIRED_COLOR, rules)
            );

        static Regex innerBagsRegex = new Regex(@"^(\d+)\s(.*)\sbags?\.?$", RegexOptions.Compiled);
        static IEnumerable<(string innerColor, int quantity)> ProcessInnerRues(string text)
        {
            if (text == "no other bags.")
                return new (string innerColor, int quantity)[0];
            return text.Split(", ").Select(innerText => {
                var match = innerBagsRegex.Match(innerText);
                if (match.Success)
                    return (match.Groups[2].Value, int.Parse(match.Groups[1].Value));
                throw new Exception($"Bad format '{innerText}'");
            });
        }

        static Regex bagsRegex = new Regex(@"^(.*)\sbags contain\s(.*)$", RegexOptions.Compiled);
        static (string color, IEnumerable<(string innerColor, int quantity)> innerRules) ProcessLine(string line)
        {
            var match = bagsRegex.Match(line);
            if (match.Success)
                return (match.Groups[1].Value, ProcessInnerRues(match.Groups[2].Value));
            throw new Exception($"Bad format '{line}'");
        }

        static Rules GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(ProcessLine).ToDictionary(
                pair => pair.color,
                pair => pair.innerRules
            );

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
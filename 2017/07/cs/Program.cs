﻿using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    record Record(int Weight, IEnumerable<string> Children);

    class Program
    {
        static string Part1(IDictionary<string, Record> records)
        {
            var allChildren = records.SelectMany(pair => pair.Value.Children).ToArray();
            return records.Keys.First(name => !allChildren.Contains(name));
        }

        static int Part2(IDictionary<string, Record> records, string topTower)
        {
            var combinedWeights = new Dictionary<string, int>();
            while (combinedWeights.Count != records.Count)
                foreach (var (name, record) in records.Where(pair => !combinedWeights.ContainsKey(pair.Key))
                                                .Select(pair => (pair.Key, pair.Value)))
                    if (!record.Children.Any())
                        combinedWeights[name] = record.Weight;
                    else if (record.Children.All(child => combinedWeights.ContainsKey(child)))
                        combinedWeights[name] = record.Children.Sum(child => combinedWeights[child]) + record.Weight;
            var currentTower = records[topTower];
            var weightDifference = 0;
            while (true)
            {
                var childrenWeights = currentTower.Children.Select(child => combinedWeights[child]).ToArray();
                var weightCounts = childrenWeights.Distinct().Select(weight => (weight, childrenWeights.Count(t => t == weight)))
                    .ToDictionary(pair => pair.Item1, pair => pair.Item2);
                if (weightCounts.Count == 1)
                    return currentTower.Weight + weightDifference;
                var singleWeight = weightCounts.First(pair => pair.Value == 1).Key;
                weightDifference = weightCounts.First(pair => pair.Value > 1).Key - singleWeight;
                currentTower = records[currentTower.Children.First(child => combinedWeights[child] == singleWeight)];
            }
        }

        static (string, int) Solve(IDictionary<string, Record> records)
        {
            var topTower = Part1(records);
            return (
                topTower,
                Part2(records, topTower)
            );
        }

        static Regex lineRegex = new Regex(@"^(?<name>[a-z]+)\s\((?<weight>\d+)\)(?: -> )?(?<children>.*)", RegexOptions.Compiled);
        static IDictionary<string, Record> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line =>
            {
                Match match = lineRegex.Match(line);
                if (match.Success)
                    return (
                        match.Groups["name"].Value,
                        int.Parse(match.Groups["weight"].Value),
                        match.Groups["children"].Value.Split(", ", StringSplitOptions.RemoveEmptyEntries));
                throw new Exception($"Bad format '{line}'");
            }).ToDictionary(trio => trio.Item1, trio => new Record(trio.Item2, trio.Item3));

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
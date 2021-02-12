﻿using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using ChemicalPortion = Tuple<int, string>;

    class DefaultDictionary<TKey, TValue>
    {
        public bool Any() => _innerDictionary.Any();

        public DefaultDictionary(Dictionary<TKey, TValue> init = default(Dictionary<TKey, TValue>))
            => _innerDictionary = init ?? new Dictionary<TKey, TValue>();

        public TValue this[TKey key]
        {
            get
            {
                if (!_innerDictionary.ContainsKey(key))
                    _innerDictionary[key] = default(TValue);
                return _innerDictionary[key];
            }
            set => _innerDictionary[key] = value;
        }

        public (TKey key, TValue value) Pop()
        {
            var result = _innerDictionary.First();
            _innerDictionary.Remove(result.Key);
            return (result.Key, result.Value);
        }

        public bool Remove(TKey key) => _innerDictionary.Remove(key);

        private IDictionary<TKey, TValue> _innerDictionary;
    }

    class Program
    {
        static long GetRequiredOre(Dictionary<string, Tuple<int, IEnumerable<ChemicalPortion>>> reactions, long requireFuel)
        {
            var requiredChemicals = new DefaultDictionary<string, long>();
            requiredChemicals["FUEL"] = requireFuel;
            var producedChemicals = new DefaultDictionary<string, long>();
            var oreCount = 0L;
            while (requiredChemicals.Any())
            {
                var (item, amount) = requiredChemicals.Pop();
                if (amount <= producedChemicals[item])
                {
                    producedChemicals[item] -= amount;
                    continue;
                }
                var amountNeeded = amount - producedChemicals[item];
                producedChemicals.Remove(item);
                var (ammoutPrduced, portions) = reactions[item];
                var requiredQuantity = (long)Math.Ceiling((double)amountNeeded / ammoutPrduced);
                producedChemicals[item] += (requiredQuantity * ammoutPrduced) - amountNeeded;
                foreach (var (otherAmountRequired, chemical) in portions)
                {
                    var chemicalValue = otherAmountRequired * requiredQuantity;
                    if (chemical == "ORE")
                        oreCount += chemicalValue;
                    else
                        requiredChemicals[chemical] += chemicalValue;
                }
            }
            return oreCount;
        }

        static long Part1(Dictionary<string, Tuple<int, IEnumerable<ChemicalPortion>>> reactions) => GetRequiredOre(reactions, 1);

        static long Part2(Dictionary<string, Tuple<int, IEnumerable<ChemicalPortion>>> reactions)
        {
            var requiredFuel = 1L;
            var lastNeeded = GetRequiredOre(reactions, requiredFuel);
            var maxOre = 1000_000_000_000;
            while (true)
            {
                requiredFuel = requiredFuel * maxOre / lastNeeded;
                var oreNeeded = GetRequiredOre(reactions, requiredFuel);
                if (lastNeeded == oreNeeded)
                    break;
                else
                    lastNeeded = oreNeeded;
            }
            return requiredFuel;
        }

        static Regex lineRegex = new Regex(@"(\d+)\s([A-Z]+)", RegexOptions.Compiled);
        static Dictionary<string, Tuple<int, IEnumerable<ChemicalPortion>>> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line => {
                var matches = new Stack<Match>(lineRegex.Matches(line));
                var result = matches.Pop();
                return (
                    result.Groups[2].Value, 
                    int.Parse(result.Groups[1].Value), 
                    matches.Select(match => Tuple.Create(int.Parse(match.Groups[1].Value), match.Groups[2].Value)));
            }).ToDictionary(group => group.Item1, group => Tuple.Create(group.Item2, group.Item3));
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
using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Instructions = Tuple<List<ValueInstruction>, Dictionary<int, CompareInstruction>>;
    record ValueInstruction(int bot, int value);
    record CompareInstruction(string lowTarget, int low, string highTarget, int high);

    class Program
    {
        const int LOW_VALUE = 17;
        const int HIGH_VALUE = 61;
        static int[] TARGET_OUTPUTS = new [] { 0, 1, 2 };
        static (bool complete, int bot) IsComplete(int test, int bot, int lowChip, int highChip, Dictionary<int, int> outputs)
        {
            if (test == 1)
            {
                if (lowChip == LOW_VALUE && highChip == HIGH_VALUE)
                    return (true, bot);
                return (false, -1);
            }
            else
            {
                if (TARGET_OUTPUTS.All(output => outputs.ContainsKey(output)))
                    return (true, TARGET_OUTPUTS.Aggregate(1, (sofar, output) => sofar * outputs[output]));
                return (false, -1);
            }
        }

        static int Run(Instructions instructions, int test)
        {
            var (valueInstructions, compareInstructions) = instructions;
            var bots = new Dictionary<int, List<int>>();
            foreach (var valueInstruction in valueInstructions)
            {
                if (! bots.ContainsKey(valueInstruction.bot))
                    bots[valueInstruction.bot] = new List<int>();
                bots[valueInstruction.bot].Add(valueInstruction.value);
            }
            var outputs = new Dictionary<int, int>();
            while (true)
            {
                var bot = bots.First(pair => pair.Value.Count == 2).Key;
                var lowChip = bots[bot].Min();
                var highChip = bots[bot].Max();
                var compareInstruction = compareInstructions[bot];
                if (compareInstruction.lowTarget == "bot")
                {
                    if (!bots.ContainsKey(compareInstruction.low))
                        bots[compareInstruction.low] = new List<int>();
                    bots[compareInstruction.low].Add(lowChip);
                }
                else
                    outputs[compareInstruction.low] = lowChip;
                if (compareInstruction.highTarget == "bot")
                {
                    if (!bots.ContainsKey(compareInstruction.high))
                        bots[compareInstruction.high] = new List<int>();
                    bots[compareInstruction.high].Add(highChip);
                }
                else
                    outputs[compareInstruction.high] = highChip;
                bots[bot].Remove(lowChip);
                bots[bot].Remove(highChip);
                var (complete, result) = IsComplete(test, bot, lowChip, highChip, outputs);
                if (complete)
                    return result;
            }
        }

        static int Part1(Instructions instructions) => Run(instructions, 1);

        static int Part2(Instructions instructions) => Run(instructions, 2);

        static Regex valueRegex = new Regex(@"^value\s(?<value>\d+)\sgoes to bot\s(?<bot>\d+)$", RegexOptions.Compiled);
        static Regex compareRegex = new Regex(@"^bot\s(?<bot>\d+)\sgives low to\s(?<lowTarget>bot|output)\s(?<low>\d+)\sand high to\s(?<highTarget>bot|output)\s(?<high>\d+)$");
        static Instructions GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var valueInstructions = new List<ValueInstruction>();
            var compareInstructions = new Dictionary<int, CompareInstruction>();
            foreach (var line in File.ReadAllLines(filePath))
            {
                var valueMatch = valueRegex.Match(line);
                if (valueMatch.Success)
                    valueInstructions.Add(new ValueInstruction(int.Parse(valueMatch.Groups["bot"].Value), int.Parse(valueMatch.Groups["value"].Value)));
                var compareMatch = compareRegex.Match(line);
                if (compareMatch.Success)
                    compareInstructions[int.Parse(compareMatch.Groups["bot"].Value)] = new CompareInstruction(
                        compareMatch.Groups["lowTarget"].Value,
                        int.Parse(compareMatch.Groups["low"].Value),
                        compareMatch.Groups["highTarget"].Value,
                        int.Parse(compareMatch.Groups["high"].Value)
                    );
            }
            return Tuple.Create(valueInstructions, compareInstructions);
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
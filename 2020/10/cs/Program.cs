using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    class Program
    {
        static int Part1(IEnumerable<int> adapters)
        {
            var diff1 = 0;
            var diff3 = 1;
            var currentJoltage = 0;
            foreach (var joltage in adapters)
            {
                var diff = joltage - currentJoltage;
                if (diff == 1)
                    diff1++;
                else if (diff == 3)
                    diff3++;
                currentJoltage = joltage;
            }
            return diff1 * diff3;
        }

        static int CalculateCombinations(int sequence)
        {
            if (sequence < 3)
                return 1;
            if (sequence == 3)
                return 2;
            return CalculateCombinations(sequence - 1) + CalculateCombinations(sequence - 2) + CalculateCombinations(sequence - 3);
        }

        static long Part2(List<int> adapters)
        {
            adapters.Add(adapters[^1]);
            var sequences = new List<int>();
            var currentSequenceLength = 1;
            var currentJoltage = 0;
            foreach (var joltage in adapters)
            {
                if (currentJoltage == joltage - 1)
                    currentSequenceLength++;
                else
                {
                    sequences.Add(currentSequenceLength);
                    currentSequenceLength = 1;
                }
                currentJoltage = joltage;
            }
            return sequences.Aggregate(1L, (soFar, current) => soFar * CalculateCombinations(current));
        }

        static (int, long) Solve(List<int> adapters)
            => (
                Part1(adapters),
                Part2(adapters)
            );

        static List<int> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(int.Parse).OrderBy(v => v).ToList();

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
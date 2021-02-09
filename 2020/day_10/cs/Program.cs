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
        static int Part1(IEnumerable<int> numbers)
        {
            var diff1 = 0;
            var diff3 = 1;
            var currentJoltage = 0;
            foreach (var number in numbers.OrderBy(n => n))
            {
                var diff = number - currentJoltage;
                if (diff == 1)
                    diff1++;
                else if (diff == 3)
                    diff3++;
                currentJoltage = number;
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

        static long Part2(IEnumerable<int> numbers)
        {
            var adapters = numbers.OrderBy(n => n).ToList();
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

        static IEnumerable<int> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(int.Parse);
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
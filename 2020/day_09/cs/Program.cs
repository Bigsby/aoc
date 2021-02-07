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
        static bool HasNoValidPair(int numberIndex, IEnumerable<long> numbers)
        {
            var number = numbers.ElementAt(numberIndex);
            foreach (var testIndex in Enumerable.Range(numberIndex - 25, 25))
            {
                var testNumber = numbers.ElementAt(testIndex);
                foreach (var pairIndex in Enumerable.Range(numberIndex - 25, 25))
                    if (pairIndex != testIndex && testNumber + numbers.ElementAt(pairIndex) == number)
                        return false;
            }
            return true;
        }

        static long Part1(IEnumerable<long> numbers)
            => numbers.ElementAt(
                Enumerable.Range(25, numbers.Count() - 25).First(index => HasNoValidPair(index, numbers)));
        
        static long GetWeakness(IEnumerable<long> numbers, long targetNumber)
        {
            var numbersArray = numbers.ToArray();
            for (var startIndex = 0; startIndex < numbers.Count(); startIndex++)
            {
                
                var currentSum = 0L;
                var length = 1;
                while (currentSum < targetNumber)
                {
                    var newSet = numbersArray[new Range(startIndex, startIndex + length)];
                    currentSum = newSet.Sum();
                    if (currentSum == targetNumber)
                        return newSet.Min() + newSet.Max();
                    length += 1;
                }
            }
            throw new Exception("Weakness not found");
        }

        static long Part2(IEnumerable<long> numbers) => GetWeakness(numbers, Part1(numbers));

        static IEnumerable<long> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(long.Parse);
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
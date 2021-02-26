using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;

namespace AoC
{
    class Program
    {
        static bool HasNoValidPair(int numberIndex, long[] numbers)
        {
            foreach (var testIndex in Enumerable.Range(numberIndex - 25, 25))
                foreach (var pairIndex in Enumerable.Range(numberIndex - 25, 25))
                    if (pairIndex != testIndex 
                        && numbers[testIndex] + numbers.ElementAt(pairIndex) == numbers[numberIndex])
                        return false;
            return true;
        }
        
        static long GetWeakness(long[] numbers, long targetNumber)
        {
            for (var startIndex = 0; startIndex < numbers.Count(); startIndex++)
            {
                var currentSum = 0L;
                var length = 1;
                while (currentSum < targetNumber)
                {
                    var newSet = numbers[new Range(startIndex, startIndex + length)];
                    currentSum = newSet.Sum();
                    if (currentSum == targetNumber)
                        return newSet.Min() + newSet.Max();
                    length += 1;
                }
            }
            throw new Exception("Weakness not found");
        }

        static (long, long) Solve(long[] numbers)
        {    
            var part1Result = numbers.ElementAt(
                Enumerable.Range(25, numbers.Count() - 25).First(index => HasNoValidPair(index, numbers)));
            return (
                part1Result,
                GetWeakness(numbers, part1Result)
            );
        }

        static long[] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(long.Parse).ToArray();

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
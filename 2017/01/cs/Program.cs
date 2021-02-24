using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;

namespace AoC
{
    class Program
    {
        static int Part1(int[] numbers)
        {
            var count = 0;
            var previous = numbers[^1];
            foreach (var number in numbers)
            {
                if (number == previous)
                {
                    count += number;
                }
                previous = number;
            }
            return count;
        }

        static int Part2(int[] numbers)
        {
            var listLength = numbers.Count();
            var halfLength = (int)Math.Floor((decimal)listLength / 2);
            numbers = numbers.Concat(numbers).ToArray();
            var count = 0;
            for (var index = 0; index < listLength; index++)
            {
                if (numbers[index] == numbers[index + halfLength])
                {
                    count += numbers[index];
                }
            }
            return count;
        }

        static int[] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim().Select(c => int.Parse(c.ToString())).ToArray();
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
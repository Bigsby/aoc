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
                if (number == previous)
                    count += number;
                else 
                    previous = number;
            return count;
        }

        static int Part2(int[] numbers)
        {
            var listLength = numbers.Count();
            var halfLength = (int)Math.Floor((decimal)listLength / 2);
            numbers = numbers.Concat(numbers).ToArray();
            var count = 0;
            for (var index = 0; index < listLength; index++)
                if (numbers[index] == numbers[index + halfLength])
                    count += numbers[index];
            return count;
        }
        
        static (int, int) Solve(int[] numbers)
            => (
                Part1(numbers),
                Part2(numbers)
            );

        static int[] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim().Select(c => int.Parse(c.ToString())).ToArray();

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
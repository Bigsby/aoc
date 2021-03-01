using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;

namespace AoC
{
    class Program
    {
        static int GetCount(int[] numbers, int indexOffset)
            => Enumerable.Range(0, numbers.Length).Aggregate(0, 
                (count, index) => numbers[index] == numbers[(index + indexOffset) % numbers.Length] ?
                    count + numbers[index]
                    :
                    count
                );

        static (int, int) Solve(int[] numbers)
            => (
                GetCount(numbers, numbers.Length - 1),
                GetCount(numbers, numbers.Length / 2)
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
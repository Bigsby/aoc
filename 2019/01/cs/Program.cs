using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;

namespace AoC
{
    class Program
    {
        static int Part1(int[] masses)
        {
            return masses.Sum(mass => mass / 3 - 2);
        }

        static int Part2(int[] masses)
        {
            return masses.Sum(mass => {
                var total = 0;
                var currentMass = mass;
                while (true)
                {
                    var fuel = currentMass / 3 - 2;
                    if (fuel <= 0)
                    {
                        break;
                    }
                    total += fuel;
                    currentMass = fuel;
                }
                return total;
            });
        }

        static int[] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(int.Parse).ToArray();
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
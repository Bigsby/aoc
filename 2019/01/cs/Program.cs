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
                        break;
                    total += fuel;
                    currentMass = fuel;
                }
                return total;
            });
        }

        static (int, int) Solve(int[] masses)
            => (
                masses.Sum(mass => mass / 3 - 2),
                masses.Sum(mass => {
                    var total = 0;
                    var currentMass = mass;
                    while (true)
                    {
                        var fuel = currentMass / 3 - 2;
                        if (fuel <= 0)
                            break;
                        total += fuel;
                        currentMass = fuel;
                    }
                    return total;
                })
            );

        static int[] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(int.Parse).ToArray();

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
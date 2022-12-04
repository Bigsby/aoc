using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = String;

    static class Program
    {
        static int Part1(Input puzzleInput)
        { 
            return 1;
        }

        static int Part2(Input puzzleInput)
        {
            return 2;
        }

        static (int, int) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim();

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

using System;
using System.Collections.Generic;
using static System.Console;
using System.Linq;
using System.IO;
using System.Diagnostics;

namespace AoC
{
    class Program
    {
        static int Part1(IEnumerable<int> directions)
        {
            var currentFloor = 0;
            foreach (var direction in directions)
            {
                currentFloor += direction;
            }
            return currentFloor;
        }

        static int Part2(IEnumerable<int> directions)
        {
            var currentFloor = 0;
            var currentPosition = 1;
            foreach (var direction in directions)
            {
                currentFloor += direction;
                if (currentFloor == -1) break;
                currentPosition += 1;
            }
            return currentPosition;
        }

        static IEnumerable<int> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim().Select(c => c == '(' ? 1 : -1);
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
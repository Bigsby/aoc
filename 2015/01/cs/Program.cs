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

        static (int, int) Solve(IEnumerable<int> directions)
            => (Part1(directions), Part2(directions));

        static IEnumerable<int> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim().Select(c => c == '(' ? 1 : -1);

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
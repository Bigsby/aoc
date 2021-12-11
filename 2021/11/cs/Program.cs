using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    static class Program
    {
        static IEnumerable<(int, int)> GetNeighbors(int x, int y)
        {
            if (x > 0)
            {
                yield return (x - 1, y);
                if (y > 0)
                    yield return (x - 1, y - 1);
                if (y < 9)
                    yield return (x - 1, y + 1);
            }
            if (x < 9)
            {
                yield return (x + 1, y);
                if (y > 0)
                    yield return (x + 1, y - 1);
                if (y < 9)
                    yield return (x + 1, y + 1);
            }
            if (y > 0)
                yield return (x, y - 1);
            if (y < 9)
                yield return (x, y + 1);
        }

        static (int, int) Solve(int[][] octopuses)
        {
            var flashes = 0;
            var allFlashes = 0;
            var step = 0;
            while (allFlashes == 0 || step <= 100)
            {
                step++;
                var stepFlashes = 0;
                Stack<(int, int)> toProcess = new Stack<(int, int)>();
                for (var y = 0; y < 10; y++)
                    for (var x = 0; x < 10; x++)
                    {
                        octopuses[y][x]++;
                        if (octopuses[y][x] == 10)
                            toProcess.Push((x, y));
                    }
                while (toProcess.Any())
                {
                    var (x, y) = toProcess.Pop();
                    if (octopuses[y][x] == 0)
                        continue;
                    stepFlashes++;
                    octopuses[y][x] = 0;
                    foreach (var (neighborX, neighborY) in GetNeighbors(x, y))
                    {
                        if (octopuses[neighborY][neighborX] == 0)
                            continue;
                        octopuses[neighborY][neighborX]++;
                        if (octopuses[neighborY][neighborX] == 10)
                            toProcess.Push((neighborX, neighborY));
                    }

                }
                if (step <= 100)
                    flashes += stepFlashes;
                if (stepFlashes == 100)
                    allFlashes = step;
            }
            return (flashes, allFlashes);
        }

        static int[][] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => line.Select(c => (int)c - (int)'0').ToArray()).ToArray();

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

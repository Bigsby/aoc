using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = string[];

    static class Program
    {
        static (int, int)[] DIRECTIONS = new [] 
        {
            (-1, -1), ( 0, -1), ( 1, -1),
            (-1,  0),           ( 1,  0),
            (-1,  1), ( 0,  1), ( 1,  1)
        };

        static bool TryGetNeighbour(Input puzzleInput, int x, int y, int goX, int goY, char letter, out (int, int) neighbour)
        {
            var newX = x + goX;
            var newY = y + goY;
            if (newX >= 0
                && newX < puzzleInput[0].Length
                && newY >= 0
                && newY < puzzleInput.Length
                && puzzleInput[newY][newX] == letter)
            {
                neighbour = (newX, newY);
                return true;
            }
            neighbour = (0, 0);
            return false;
        }

        static char[] LETTERS = new [] { 'M', 'A', 'S' };

        static bool HasXMAS(Input puzzleInput, int x, int y, int goX, int goY)
        {
            (int X, int Y) neighbour = (x, y);
            foreach (var letter in LETTERS)
                if (!TryGetNeighbour(puzzleInput, neighbour.X, neighbour.Y, goX, goY, letter, out neighbour))
                    return false;
            return true;
        }

        static int Part1(Input puzzleInput)
        { 
            var width = puzzleInput[0].Length;
            var height = puzzleInput.Length;
            var total = 0;
            for (var y = 0; y < height; y++)
                for (var x = 0; x < width; x++)
                {
                    if (puzzleInput[y][x] != 'X')
                        continue;
                    foreach (var (goX, goY) in DIRECTIONS)
                        if (HasXMAS(puzzleInput, x, y, goX, goY))
                            total++;
                }
            return total;
        }

        static bool Has_MAS(Input puzzleInput, int x, int y, int goX, int goY)
            => TryGetNeighbour(puzzleInput, x, y, goX, goY, 'M', out _)
               &&
               TryGetNeighbour(puzzleInput, x, y, -goX, -goY, 'S', out _)
               ||
               TryGetNeighbour(puzzleInput, x, y, goX, goY, 'S', out _)
               &&
               TryGetNeighbour(puzzleInput, x, y, -goX, -goY, 'M', out _);

        static bool HasX_MAS(Input puzzleInput, int x, int y)
            => Has_MAS(puzzleInput, x, y, 1, 1)
               &&
               Has_MAS(puzzleInput, x, y, -1, 1);

        static int Part2(Input puzzleInput)
        {
            var width = puzzleInput[0].Length;
            var height = puzzleInput.Length;
            var total = 0;
            for (var y = 0; y < height; y++)
                for (var x = 0; x < width; x++)
                    if (puzzleInput[y][x] == 'A' && HasX_MAS(puzzleInput, x, y))
                        total++;
            return total;
        }

        static (int, int) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => line.Trim()).ToArray();

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

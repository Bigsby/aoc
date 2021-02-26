using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    class Program
    {
        static int Part1(int targetNumber)
        {
            var side = (int)Math.Floor(Math.Sqrt(targetNumber)) + 1;
            var pastLastSquare = targetNumber - (int)Math.Pow((side - 1), 2);
            var halfSide = side / 2;
            if (pastLastSquare >= side)
                pastLastSquare -= side;
            var offsetToMiddle = Math.Abs(halfSide - pastLastSquare);
            return halfSide + offsetToMiddle;
        }

        static Complex I = Complex.ImaginaryOne;
        static Complex[] DIRECTIONS = {
            -1 - I, - I, 1 - I,
            -1,          1,
            -1 + I,   I, 1 + I
        };
        static int GetSumForNeighbors(Dictionary<Complex, int> grid, Complex position)
        {
            return DIRECTIONS.Select(direction => direction + position)
                .Sum(neighbor => grid.ContainsKey(neighbor) ? grid[neighbor] : 0);
        }

        static int Part2(int targetNumber)
        {
            var grid = new Dictionary<Complex, int> { { 0, 1 } };
            Complex position = 0;
            Complex direction = 1;
            var movesInDirection = 1;
            while (true)
            {
                foreach (var length in Enumerable.Range(0, 2))
                {
                    direction *= I;
                    foreach (var _ in Enumerable.Range(0, movesInDirection))
                    {
                        position += direction;
                        grid[position] = GetSumForNeighbors(grid, position);
                        if (grid[position] > targetNumber)
                            return grid[position];
                    }
                }
                movesInDirection += 1;
            }
        }

        static (int, int) Solve(int targetNumber)
            => (
                Part1(targetNumber),
                Part2(targetNumber)
            );

        static int GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : int.Parse(File.ReadAllText(filePath).Trim());

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
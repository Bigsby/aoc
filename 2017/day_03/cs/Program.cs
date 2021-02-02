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
            Complex move = 1;
            var movesInDirection = 1;
            while (true)
            {
                foreach (var length in Enumerable.Range(0, 2))
                {
                    move *= I;
                    foreach (var _ in Enumerable.Range(0, movesInDirection))
                    {
                        position += move;
                        grid[position] = GetSumForNeighbors(grid, position);
                        if (grid[position] > targetNumber)
                            return grid[position];
                    }
                }
                movesInDirection += 1;
            }
        }

        static int GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return int.Parse(File.ReadAllText(filePath).Trim());
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
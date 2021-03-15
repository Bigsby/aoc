using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Drawing;

namespace AoC
{
    class Program
    {
        const int GRID_SIZE = 300;

        static int GetIndex(int x, int y) => y * GRID_SIZE + x;

        static int CalculatePowerLevel(int x, int y, int serialNumber)
        {
            var rackId = x + 10;
            var powerLevel = rackId * y;
            powerLevel += serialNumber;
            powerLevel *= rackId;
            powerLevel = (powerLevel % 1000) / 100;
            return powerLevel - 5;
        }

        static int[] BuildGrid(int serialNumber)
            => Enumerable.Range(0, GRID_SIZE).SelectMany(y => Enumerable.Range(0, GRID_SIZE).Select(x => (x, y)))
                .Select((pair) => CalculatePowerLevel(pair.x + 1, pair.y + 1, serialNumber))
                .ToArray();

        static int[] BuildSummedAreaTable(int[] grid)
        {
            for (var y = 0; y < GRID_SIZE; y++)
                for (var x = 0; x < GRID_SIZE; x++)
                    grid[GetIndex(x, y)] =
                                            grid[GetIndex(x,     y)] +
                                   (x > 0 ? grid[GetIndex(x - 1, y)] : 0) +
                                   (y > 0 ? grid[GetIndex(x    , y - 1)] : 0) +
                        - (x > 0 && y > 0 ? grid[GetIndex(x - 1, y - 1)] : 0);
            return grid;
        }

        static int SumFromAreaTable(int[] grid, int x, int y, int size)
            => grid[GetIndex(x - 1       , y - 1)]
             - grid[GetIndex(x - 1 + size, y - 1)]
             - grid[GetIndex(x - 1       , y - 1 + size)]
             + grid[GetIndex(x - 1 + size, y - 1 + size)];

        static (string, string) Solve(int serialNumber)
        {
            var grid = BuildGrid(serialNumber);
            var summedAreaTable = BuildSummedAreaTable(grid);
            var maxFuel = 0;
            var maxSize = 0;
            var maxCell = (-1, -1);
            var max3Cell = (-1, -1);
            var max3Fuel = 0;
            foreach (var size in Enumerable.Range(1, GRID_SIZE - 1))
                foreach (var (x, y) in Enumerable.Range(1, GRID_SIZE - size - 1)
                                    .SelectMany(x => Enumerable.Range(1, GRID_SIZE - size - 1).Select(y => (x, y))))
                {
                    var fuel = SumFromAreaTable(summedAreaTable, x, y, size);
                    if (fuel > maxFuel)
                    {
                        maxFuel = fuel;
                        maxCell = (x + 1, y + 1);
                        maxSize = size;
                    }
                    if (size == 3 && fuel > max3Fuel)
                    {
                        max3Fuel = fuel;
                        max3Cell = (x + 1, y + 1);
                    }
                }
            return ($"{max3Cell.Item1},{max3Cell.Item2}", $"{maxCell.Item1},{maxCell.Item2},{maxSize}");
        }

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
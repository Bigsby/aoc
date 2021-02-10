﻿using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Drawing;

namespace AoC
{
    using Grid = Dictionary<Point, int>;
    class Program
    {
        const int GRID_SIZE = 300;

        static int CalculatePowerLevel(int x, int y, int serialNumber)
        {
            var rackId = x + 10;
            var powerLevel = rackId * y;
            powerLevel += serialNumber;
            powerLevel *= rackId;
            powerLevel = (powerLevel % 1000) / 100;
            return powerLevel - 5;
        }

        static Grid BuildGrid(int serialNumber)
            => Enumerable.Range(0, GRID_SIZE).SelectMany(y => Enumerable.Range(0, GRID_SIZE).Select(x => (x, y)))
                .ToDictionary(pair => new Point(pair.x, pair.y), pair => CalculatePowerLevel(pair.x + 1, pair.y + 1, serialNumber));

        static Grid BuildSummedAreaTable(Grid grid)
        {
            for (var y = 0; y < GRID_SIZE; y++)
                for (var x = 0; x < GRID_SIZE; x++)
                    grid[new Point(x, y)] =
                                            grid[new Point(x    , y    )] +
                                   (x > 0 ? grid[new Point(x - 1, y    )] : 0) +
                                   (y > 0 ? grid[new Point(x    , y - 1)] : 0) +
                        - (x > 0 && y > 0 ? grid[new Point(x - 1, y - 1)] : 0);
            return grid;
        }

        static int SumFromAreaTable(Grid grid, int x, int y, int size)
            => grid[new Point(x - 1       , y - 1       )]
             - grid[new Point(x - 1 + size, y - 1       )]
             - grid[new Point(x - 1       , y - 1 + size)]
             + grid[new Point(x - 1 + size, y - 1 + size)];

        static ((int x, int y), int size) FindLargestPower(int serialNumber, IEnumerable<int> sizes)
        {
            var grid = BuildGrid(serialNumber);
            var summedAreaTable = BuildSummedAreaTable(grid);
            var maxFuel = 0;
            var maxSize = 0;
            var maxCell = (-1, -1);
            foreach (var size in sizes)
                foreach (var (x, y) in Enumerable.Range(1, GRID_SIZE - size - 1)
                                        .SelectMany(y => Enumerable.Range(1, GRID_SIZE - size - 1).Select(x => (x, y))))
                {
                    var fuel = SumFromAreaTable(summedAreaTable, x, y, size);
                    if (fuel > maxFuel)
                    {
                        maxFuel = fuel;
                        maxCell = (x + 1, y + 1);
                        maxSize = size;
                    }
                }
            return (maxCell, maxSize);
        }

        static string Part1(int serialNumber)
        {
            var ((x, y), _) = FindLargestPower(serialNumber, new [] { 3 });
            return $"{x},{y}";
        }

        static string Part2(int serialNumber)
        {
            var ((x, y), size) = FindLargestPower(serialNumber, Enumerable.Range(1, GRID_SIZE - 1));
            return $"{x},{y},{size}";
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
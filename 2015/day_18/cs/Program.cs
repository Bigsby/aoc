﻿using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Grid = Dictionary<Complex,bool>;

    static class Program
    {
        static void PrintGrid(Grid grid)
        {
            var maxX = (int)grid.Keys.Max(p => p.Real) + 1;
            var maxY = (int)grid.Keys.Max(p => p.Imaginary) + 1;
            for (var y = 0; y < maxY; y++)
            {
                for (var x = 0; x < maxX; x++)
                    Write(grid[new Complex(x, y)] ? '#' : '.');
                WriteLine();
            }
            WriteLine();
            ReadLine();
        }

        static Complex[] NEIGHBOR_DIRECTIONS = new [] {
            new Complex(-1, -1),
            new Complex( 0, -1),
            new Complex( 1, -1),
            new Complex(-1,  0),
            new Complex( 1,  0),
            new Complex(-1,  1),
            new Complex( 0,  1),
            new Complex( 1,  1)
        };
        static IEnumerable<Complex> GetNeighbors(Complex position)
            => NEIGHBOR_DIRECTIONS.Select(direction => position + direction);

        static Grid GetNextState(Grid grid, IEnumerable<Complex> alwaysOn)
        {
            foreach(var position in alwaysOn)
                grid[position] = true;
            var newState = new Grid();
            foreach (var position in grid.Keys)
            {
                var neighborCount = GetNeighbors(position).Count(neighbor => grid.ContainsKey(neighbor) && grid[neighbor]);
                if (grid[position])
                    newState[position] = neighborCount == 2 || neighborCount == 3;
                else
                    newState[position] = neighborCount == 3;
            }
            foreach(var position in alwaysOn)
                newState[position] = true;
            return newState;
        }

        static int RunSteps(Grid grid, IEnumerable<Complex> alwaysOn = default(List<Complex>))
        {
            alwaysOn ??= new Complex[0];
            foreach (var _ in Enumerable.Range(0, 100))
                grid = GetNextState(grid, alwaysOn);
            return  grid.Values.Count(v => v);
        }

        static int Part1(Grid grid) => RunSteps(grid);

        static int Part2(Grid grid)
        {
            var side = (int)grid.Keys.Max(p => p.Real);
            return RunSteps(grid, new [] {
                Complex.Zero,
                new Complex(0, side),
                new Complex(side, 0),
                new Complex(side, side)
            });
        }

        static Grid GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var grid = new Grid();
            foreach (var (line, y) in File.ReadLines(filePath).Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                    grid[new Complex(x, y)] = c == '#';
            return grid;
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

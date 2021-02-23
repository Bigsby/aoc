﻿using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    static class Program
    {
        static int Part1(IEnumerable<(int, int, int, int)> points)
        {
            var edges = Enumerable.Range(0, points.Count()).Select(_ => new List<int>()).ToArray();
            foreach (var ((w0, x0, y0, z0), thisPoint) in points.Select((point, index) => (point, index)))
                foreach (var ((w1, x1, y1, z1), thatPoint) in points.Select((point, index) => (point, index)))
                    if (Math.Abs(w0 - w1) + Math.Abs(x0 - x1) + Math.Abs(y0 - y1) + Math.Abs(z0 - z1) < 4)
                        edges[thisPoint].Add(thatPoint);
            var visited = new List<int>();
            var constellations = 0;
            foreach (var thisPoint in Enumerable.Range(0, points.Count()))
            {
                if (visited.Contains(thisPoint))
                    continue;
                constellations += 1;
                var queue = new Queue<int>();
                queue.Enqueue(thisPoint);
                while (queue.Any())
                {
                    var currentPoint = queue.Dequeue();
                    if (visited.Contains(currentPoint))
                        continue;
                    visited.Add(currentPoint);
                    foreach (var other in edges[currentPoint])
                        queue.Enqueue(other);
                }
            }
            return constellations;
        }

        static object Part2(object puzzleInput) => null;

        static IEnumerable<(int, int, int, int)> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line => {
                var split = line.Split(',');
                return (
                    int.Parse(split[0]),
                    int.Parse(split[1]),
                    int.Parse(split[2]),
                    int.Parse(split[3])
                );
            });
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

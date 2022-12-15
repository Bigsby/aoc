using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<(int sensorX, int sensorY, int beaconX, int beaconY)>;
    using Data = IEnumerable<(int sensorX, int sensorY, int distance)>;

    static class Program
    {
        static int GetManhatanDistance(int x1, int y1, int x2, int y2)
            => (int)(Math.Abs(x1 - x2) + Math.Abs(y1 - y2));

        static int Part1(Data data)
        {
            const int LINE = 2_000_000; // 10 for example input
            return data.Max(a => a.sensorX - Math.Abs(LINE - a.sensorY) + a.distance)
                - data.Min(a => a.sensorX + Math.Abs(LINE - a.sensorY) - a.distance);
        }

        static long Part2(Data data)
        {
            const int MIN = 0;
            const int MAX = 4_000_000; // 20 for example input
            foreach (var a in data)
                foreach (var b in data)
                {
                    var crossDistanceA = a.sensorX - a.sensorY - a.distance;
                    var crossDistanceB = b.sensorX + b.sensorY + b.distance;
                    var beaconX = (crossDistanceB + crossDistanceA) / 2;
                    var beaconY = (crossDistanceB - crossDistanceA) / 2 + 1;
                    if ((MIN < beaconX && beaconX < MAX) && (MIN < beaconY && beaconY < MAX) &&
                        data.All(c => GetManhatanDistance(beaconX, beaconY, c.sensorX, c.sensorY) > c.distance))
                        return 4_000_000L * beaconX + beaconY;
                }
            throw new Exception("Beacon not found!");
        }

        static (int, long) Solve(Input puzzleInput)
        {
            var data = puzzleInput.Select(a =>
                (a.sensorX, a.sensorY, GetManhatanDistance(a.sensorX, a.sensorY, a.beaconX, a.beaconY)));
            return (Part1(data), Part2(data));
        }

        static int GetValue(string text)
            => int.Parse(text.Trim(',', ':').Split('=')[1]);

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line =>
            {
                var splits = line.Split(' ');
                return (GetValue(splits[2]), GetValue(splits[3]), GetValue(splits[8]), GetValue(splits[9]));
            });

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

using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Nanobots = IEnumerable<(int x, int y, int z, int r)>;

    static class Program
    {
        static int Part1(Nanobots nanobots)
        {
            var strongestBot = nanobots.Aggregate((0, 0, 0, 0), (soFar, bot) => bot.r > soFar.Item4 ? bot : soFar);
            var (x0, y0, z0, radius) = strongestBot;
            var inRange = 0;
            foreach (var (x1, y1, z1, _) in nanobots)
                if (radius >= Math.Abs(x0 - x1) + Math.Abs(y0 - y1) + Math.Abs(z0 - z1))
                    inRange++;
            return inRange;
        }

        static int Part2(Nanobots nanobots)
        {
            var xs = nanobots.Select(bot => bot.x);
            var ys = nanobots.Select(bot => bot.y);
            var zs = nanobots.Select(bot => bot.z);
            var (minX, maxX) = (xs.Min(), xs.Max() + 1);
            var (minY, maxY) = (ys.Min(), ys.Max() + 1);
            var (minZ, maxZ) = (zs.Min(), zs.Max() + 1);
            var locationRadius = 1;
            while (locationRadius < xs.Max() - xs.Min())
                locationRadius *= 2;
            while (true)
            {
                var hightestCount = 0;
                (int x, int y, int z) bestLocation = (0, 0, 0);
                var shortestDistance = -1;
                for (var x = minX; x < maxX; x += locationRadius)
                    for (var y = minY; y < maxY; y += locationRadius)
                        for (var z = minZ; z < maxZ; z += locationRadius)
                        {
                            var count = 0;
                            foreach (var (botX, botY, botZ, botRadius) in nanobots)
                            {
                                var botDistance = Math.Abs(x - botX) + Math.Abs(y - botY) + Math.Abs(z - botZ);
                                if ((botDistance - botRadius) / locationRadius <= 0)
                                    count++;
                            }
                            var locationDistance = Math.Abs(x) + Math.Abs(y) + Math.Abs(z);
                            if (count > hightestCount || (count == hightestCount && (shortestDistance == -1 || locationDistance < shortestDistance)))
                            {
                                hightestCount = count;
                                shortestDistance = locationDistance;
                                bestLocation = (x, y, z);
                            }
                        }
                if (locationRadius == 1)
                    return shortestDistance;
                minX = bestLocation.x - locationRadius;
                maxX = bestLocation.x + locationRadius + 1;
                minY = bestLocation.y - locationRadius;
                maxY = bestLocation.y + locationRadius + 1;
                minZ = bestLocation.z - locationRadius;
                maxZ = bestLocation.z + locationRadius + 1;
                locationRadius = locationRadius / 2;
            }
        }

        static Nanobots GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line => {
                var matches = Regex.Matches(line, @"-?\d+");
                return (
                    int.Parse(matches[0].Value),
                    int.Parse(matches[1].Value),
                    int.Parse(matches[2].Value),
                    int.Parse(matches[3].Value)
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

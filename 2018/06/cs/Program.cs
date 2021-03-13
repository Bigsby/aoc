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
        static int GetManhatanDistance(Complex locationA, Complex locationB)
            => (int)(Math.Abs(locationA.Real - locationB.Real) + Math.Abs(locationA.Imaginary - locationB.Imaginary));
        
        static (int startX, int endX, int startY, int endY) GetMapEdges(IEnumerable<Complex> locations)
            => (
                (int)locations.Min(l => l.Real) - 1,
                (int)locations.Max(l => l.Real) + 1,
                (int)locations.Min(l => l.Imaginary) - 1,
                (int)locations.Max(l => l.Imaginary) + 1
            );
        
        static int FindClosestLocation(Complex mapLocation, IEnumerable<Complex> locations)
        {
            var closest = -1;
            var closestDistance = int.MaxValue;
            foreach (var (location, index) in locations.Select((location, index) => (location, index)))
            {
                var distance = GetManhatanDistance(mapLocation, location);
                if (distance < closestDistance)
                {
                    closest = index;
                    closestDistance = distance;
                } else if (distance == closestDistance)
                    closest = -1;
            }
            return closest;
        }

        static int Part1(IEnumerable<Complex> locations)
        {
            var (startX, endX, startY, endY) = GetMapEdges(locations);
            var mapLocations = new Dictionary<Complex, int>();
            var locationCounts = new int[locations.Count()];
            foreach (var (y, x) in Enumerable.Range(startY, endY - startY + 1)
                .SelectMany(y => Enumerable.Range(startX, endX - startX + 1).Select(x => (y, x))))
            {
                var mapLocation = new Complex(x, y);
                var closest = FindClosestLocation(mapLocation, locations);
                mapLocations[mapLocation] = closest;
                if (closest != -1)
                    locationCounts[closest]++;
            }
            var edgeLocations = new HashSet<int>();
            foreach (var y in Enumerable.Range(startY, endY - startY + 1))
            {
                edgeLocations.Add(mapLocations[startX + Complex.ImaginaryOne * y]);
                edgeLocations.Add(mapLocations[endX + Complex.ImaginaryOne * y]);
            }
            foreach (var x in Enumerable.Range(startX, endX - startX + 1))
            {
                edgeLocations.Add(mapLocations[x + Complex.ImaginaryOne * startY]);
                edgeLocations.Add(mapLocations[x + Complex.ImaginaryOne * endY]);
            }
            return locationCounts.Where((count, index) => !edgeLocations.Contains(index)).Max();
        }

        const int MAX_DISTANCE = 10000;
        static int Part2(IEnumerable<Complex> locations)
        {
            var (startX, endX, startY, endY) = GetMapEdges(locations);
            var validLocationsCount = 0;
            foreach (var (y, x) in Enumerable.Range(startY, endY - startY + 1)
                .SelectMany(y => Enumerable.Range(startX, endX - startX + 1).Select(x => (y, x))))
            {
                var mapLocation = x + y * Complex.ImaginaryOne;
                var totalDistances = locations.Sum(location => GetManhatanDistance(mapLocation, location));
                if (totalDistances < MAX_DISTANCE)
                    validLocationsCount++;
            }
            return validLocationsCount;
        }

        static (int, int) Solve(IEnumerable<Complex> locations)
            => (
                Part1(locations),
                Part2(locations)
            );

        static IEnumerable<Complex> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => {
                var split = line.Split(',');
                return new Complex(int.Parse(split[0].Trim()), int.Parse(split[1].Trim()));
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
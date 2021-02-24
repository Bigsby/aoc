using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Asteroid = Complex;

    class Program
    {
        static int GCD(int a, int b)
        {
            while (a != 0 && b != 0)
            {
                if (a > b)
                    a %= b;
                else
                    b %= a;
            }
            return a | b;
        }

        static int GetVisibleCount(Asteroid asteroid, IEnumerable<Asteroid> asteroids, int maxX, int maxY)
        {
            var asteroidList = asteroids.Where(a => a != asteroid).ToList();
            var visibleCount = 0;
            while (asteroidList.Any())
            {
                var asteroidToCheck = asteroidList.Last();
                asteroidList.Remove(asteroidToCheck);
                visibleCount++;
                var delta = asteroidToCheck - asteroid;
                var jump = delta / GCD((int)Math.Abs(delta.Real), (int)Math.Abs(delta.Imaginary));
                asteroidToCheck = asteroid + jump;
                while (asteroidToCheck.Real >= 0 && asteroidToCheck.Real <= maxX
                    && asteroidToCheck.Imaginary >= 0 && asteroidToCheck.Imaginary <= maxY)
                {
                    asteroidList.Remove(asteroidToCheck);
                    asteroidToCheck += jump;
                }
            }
            return visibleCount;
        }

        static (int maxVisibleCount, Asteroid monitoringStation) GetMonitoringStation(IEnumerable<Asteroid> asteroids)
        {
            var maxX = (int)asteroids.Max(asteroid => asteroid.Real);
            var maxY = (int)asteroids.Max(asteroid => asteroid.Imaginary);
            var maxVisibleCount = 0;
            var monitoringStation = new Complex(-1, -1);
            foreach (var asteroid in asteroids)
            {
                var visibleCount = GetVisibleCount(asteroid, asteroids, maxX, maxY);
                if (visibleCount > maxVisibleCount)
                {
                    maxVisibleCount = visibleCount;
                    monitoringStation = asteroid;
                }
            }
            return (maxVisibleCount, monitoringStation);
        }

        static int Part1(IEnumerable<Asteroid> asteroids) => GetMonitoringStation(asteroids).maxVisibleCount;

        static double Modulo(double a, double n) => a - Math.Floor(a / n) * n;

        static int Part2(IEnumerable<Asteroid> asteroids)
        {
            var monitoringStation = GetMonitoringStation(asteroids).monitoringStation;
            var asteroidAngleDistances = new Dictionary<Asteroid, (double angle, int distance)>();
            foreach (var asteroid in asteroids.Where(a => a != monitoringStation))
            {
                var delta = asteroid - monitoringStation;
                asteroidAngleDistances[asteroid] = (
                    Math.Atan2(delta.Real, delta.Imaginary) + Math.PI,
                    (int)(Math.Abs(delta.Real) + Math.Abs(delta.Imaginary))
                );
            }
            var targetCount = 1;
            var angle = 2 * Math.PI;
            var lastRemoved = new Complex(-1, -1);
            while (targetCount <= 200)
            {
                var ordered = asteroidAngleDistances
                    .OrderBy(pair => angle == pair.Value.angle || targetCount == 1)
                    .ThenBy(pair => Modulo(angle - pair.Value.angle, 2 * Math.PI))
                    .ThenBy(pair => pair.Value.distance);
                var (asteroid, angleDistance) = ordered.First();
                asteroidAngleDistances.Remove(asteroid);
                lastRemoved = asteroid;
                angle = angleDistance.angle;
                targetCount++;
            }
            return (int)(100 * (lastRemoved.Real) + lastRemoved.Imaginary);
        }

        static IEnumerable<Asteroid> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            foreach (var yPair in File.ReadAllLines(filePath).Select((line, y) => (line, y)))
                foreach (var xPair in yPair.line.Select((c, x) => (c, x)))
                    if (xPair.c == '#')
                        yield return new Asteroid(xPair.x, yPair.y);
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
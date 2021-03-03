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
        static Complex ProcessDirection(HashSet<Complex> visitedHouses, Complex position, Complex direction)
        {
            position += direction;
            visitedHouses.Add(position);
            return position;
        }

        static int Part1(Complex[] directions)
        {
            var visitedHouses = new HashSet<Complex> { 0 };
            Complex position = 0;
            foreach (var direction in directions)
                position = ProcessDirection(visitedHouses, position, direction);
            return visitedHouses.Count;
        }

        static int Part2(Complex[] directions)
        {
            var visitedHouses = new HashSet<Complex> { 0 };
            Complex santaPosition = 0, robotPosition = 0;
            foreach (var (direction, index) in directions.Select((direction, index) => (direction, index)))
                if (index % 2 == 1)
                    santaPosition = ProcessDirection(visitedHouses, santaPosition, direction);
                else
                    robotPosition = ProcessDirection(visitedHouses, robotPosition, direction);
            return visitedHouses.Count;
        }

        static (int, int) Solve(Complex[] directions)
            => (Part1(directions), Part2(directions));

        static Dictionary<char, Complex> DIRECTIONS = new Dictionary<char, Complex> {
            { '^', -Complex.ImaginaryOne },
            { 'v', Complex.ImaginaryOne },
            { '>',  1 },
            { '<', -1 }
        };
        static Complex[] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim().Select(c => DIRECTIONS[c]).ToArray();

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
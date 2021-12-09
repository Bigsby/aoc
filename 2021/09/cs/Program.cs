using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    record Input(IDictionary<Complex, int> map, int maxX, int maxY);
    static class Program
    {
        static IEnumerable<Complex> GetNeighbors(Complex position, int maxX, int maxY)
        {
            if (position.Real > 0)
                yield return new Complex(position.Real - 1, position.Imaginary);
            if (position.Imaginary > 0)
                yield return new Complex(position.Real, position.Imaginary - 1);
            if (position.Real < maxX - 1)
                yield return new Complex(position.Real + 1, position.Imaginary);
            if (position.Imaginary < maxY - 1)
                yield return new Complex(position.Real, position.Imaginary + 1);
        }

        static int GetPositionRisk(Input input, Complex position)
        {
            var height = input.map[position];
            foreach (var neighbor in GetNeighbors(position, input.maxX, input.maxY))
                if (input.map[neighbor] <= height)
                    return 0;
            return height + 1;
        }

        static int GetBasinSize(Input input, Complex position)
        {
            var toVisit = new Queue<Complex>();
            var visited = new List<Complex>();
            toVisit.Enqueue(position);
            while (toVisit.TryDequeue(out var current))
            {
                if (visited.Contains(current))
                    continue;
                visited.Add(current);
                var currentHeight = input.map[current];
                foreach (var neighbor in GetNeighbors(current, input.maxX, input.maxY))
                {
                    var neighborHeight = input.map[neighbor];
                    if (neighborHeight == 9 || neighborHeight <= currentHeight || visited.Contains(neighbor))
                        continue;
                    toVisit.Enqueue(neighbor);
                }
            }
            return visited.Count();
        }

        static (int, int) Solve(Input puzzleInput)
        {
            var lowestSum = 0;
            var sizes = new List<int>();
            for (var y = 0; y < puzzleInput.maxY; y++)
                for (var x = 0; x < puzzleInput.maxX; x++)
                {
                    var position = new Complex(x, y);
                    var positionRisk = GetPositionRisk(puzzleInput, position);
                    if (positionRisk > 0)
                    {
                        lowestSum += positionRisk;
                        sizes.Add(GetBasinSize(puzzleInput, position));
                    }
                }

            sizes = sizes.OrderByDescending(size => size).ToList();
            return (lowestSum, sizes[0] * sizes[1] * sizes[2]);
        }

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var maxX = 0;
            var map = new Dictionary<Complex, int>();
            var position = Complex.Zero;
            foreach (var line in File.ReadAllLines(filePath))
            {
                foreach (var height in line)
                {
                    if (height == '\n')
                        continue;
                    map[position] = (int)height - (int)'0';
                    position += 1;
                }
                maxX = (int)Math.Max(position.Real, maxX);
                position = new Complex(0, position.Imaginary + 1);
            }
            return new Input(map, maxX, (int)position.Imaginary);
        }

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

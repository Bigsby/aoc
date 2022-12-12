using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Input = Tuple<Dictionary<Complex, int>, Complex, Complex>;

    static class Program
    {
        static Complex[] DIRECTIONS = new[] {
            new Complex(-1, 0),
            new Complex(0, -1),
            new Complex(1, 0),
            new Complex(0, 1)
        };

        static int FindShortestPath(Dictionary<Complex, int> heightMap, Complex start, Complex end)
        {
            var visited = new HashSet<Complex>();
            visited.Add(start);
            var queue = new Queue<(Complex, IEnumerable<Complex>)>();
            queue.Enqueue((start, new[] { start }));
            while (queue.Any())
            {
                var (position, path) = queue.Dequeue();
                foreach (var direction in DIRECTIONS)
                {
                    var newPosition = position + direction;
                    if (visited.Contains(newPosition)
                        || !heightMap.ContainsKey(newPosition)
                        || heightMap[newPosition] - heightMap[position] > 1)
                        continue;
                    if (newPosition == end)
                        return path.Count();
                    visited.Add(newPosition);
                    queue.Enqueue((newPosition, path.Concat(new[] { newPosition })));
                }
            }
            return int.MaxValue;
        }

        static int Part1(Input puzzleInput)
        {
            var (heightMap, start, end) = puzzleInput;
            return FindShortestPath(heightMap, start, end);
        }

        static int Part2(Input puzzleInput)
        {
            var (heightMap, _, end) = puzzleInput;
            var shortestPath = int.MaxValue;
            foreach (var (position, height) in heightMap)
                if (height == 'a')
                    shortestPath = Math.Min(shortestPath, FindShortestPath(heightMap, position, end));
            return shortestPath;
        }

        static (int, int) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var heightMap = new Dictionary<Complex, int>();
            var position = Complex.Zero;
            var start = Complex.Zero;
            var end = Complex.Zero;
            foreach (var line in File.ReadAllLines(filePath))
            {
                foreach (var c in line)
                {
                    switch (c)
                    {
                        case 'S':
                            start = position;
                            heightMap[position] = 'a';
                            break;
                        case 'E':
                            end = position;
                            heightMap[position] = 'z';
                            break;
                        default:
                            heightMap[position] = c;
                            break;
                    }
                    position += 1;
                }
                position = new Complex(0, position.Imaginary + 1);
            }
            return Tuple.Create(heightMap, start, end);
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

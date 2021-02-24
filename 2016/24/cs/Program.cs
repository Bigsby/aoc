using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Maze = IEnumerable<Complex>;
    using Numbers = Dictionary<Complex, int>;

    static class Program
    {
        static Complex[] DIRECTIONS = new [] { -1, -Complex.ImaginaryOne, 1, Complex.ImaginaryOne };
        static Dictionary<int, int> FindPathsFromLocation(Maze maze, Numbers numbers, Complex start)
        {
            var visited = new List<Complex>();
            visited.Add(start);
            var queue = new Queue<(Complex, int)>();
            queue.Enqueue((start, 0));
            var paths = new Dictionary<int, int>();
            while (queue.Any())
            {
                var (position, distance) = queue.Dequeue();
                foreach (var newPosition in DIRECTIONS.Select(direction => position + direction))
                    if (maze.Contains(newPosition) && !visited.Contains(newPosition))
                    {
                        visited.Add(newPosition);
                        if (numbers.TryGetValue(newPosition, out var number))
                            paths[number] = distance + 1;
                        queue.Enqueue((newPosition, distance + 1));
                    }
            }
            return paths;
        }

        static int GetStepsForPath(IEnumerable<int> path, Dictionary<int, Dictionary<int, int>> pathsFromNumbers)
        {
            var steps = 0;
            var current = 0;
            var pathQueue = new Queue<int>(path);
            while (pathQueue.Any())
            {
                var next = pathQueue.Dequeue();
                steps += pathsFromNumbers[current][next];
                current = next;
            }
            return steps;
        }

        static IEnumerable<IEnumerable<T>> Permutations<T>(IEnumerable<T> values) where T : IComparable
        {
            if (values.Count() == 1)
                return new[] { values };
            return values.SelectMany(v =>
                Permutations(values.Where(x => x.CompareTo(v) != 0)), (v, p) => p.Prepend(v));
        }

        static int FindLeastSteps((Maze, Numbers) data, bool returnHome)
        {
            var (maze, numbers) = data;
            var pathsFromNumbers = numbers.ToDictionary(pair => pair.Value, pair => FindPathsFromLocation(maze, numbers, pair.Key));
            var numbersBesidesStart = numbers.Values.Where(number => number != 0);
            var minumSteps = int.MaxValue;
            foreach (var combination in Permutations(numbersBesidesStart))
            {
                var pathList = combination.ToList();
                if (returnHome)
                    pathList.Add(0);
                minumSteps = Math.Min(minumSteps, GetStepsForPath(pathList, pathsFromNumbers));
            }
            return minumSteps;
        }

        static int Part1((Maze, Numbers) data) => FindLeastSteps(data, false);

        static int Part2((Maze, Numbers) data) => FindLeastSteps(data, true);

        static (Maze, Numbers) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var maze = new List<Complex>();
            var numbers = new Numbers();
            foreach (var (line, y) in File.ReadLines(filePath).Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                {
                    var location = new Complex(x, y);
                    if (c == '.')
                        maze.Add(location);
                    else if (char.IsDigit(c))
                    {
                        numbers[location] = int.Parse(c.ToString());
                        maze.Add(location);
                    }
                }
            return (maze, numbers);
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

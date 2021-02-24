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
        static bool IsPositionValid(Complex position, int number)
        {
            var (x, y) = ((int)position.Real, (int)position.Imaginary);
            if (x < 0 || y < 0)
                return false;
            var value = x * x + 3 * x + 2 * x * y + y + y * y + number;
            return Convert.ToString(value, 2).Count(c => c == '1') % 2 == 0;
        }

        static Complex[] DIRECTIONS = new[] {
            -1, Complex.ImaginaryOne, -Complex.ImaginaryOne, 1
        };

        static int Part1(int number)
        {
            var startPosition = new Complex(1, 1);
            var queue = new Queue<Tuple<Complex, List<Complex>>>();
            queue.Enqueue(Tuple.Create(startPosition, new List<Complex> { startPosition }));
            var target = new Complex(31, 39);
            while (queue.Any())
            {
                var (position, visited) = queue.Dequeue();
                foreach (var direction in DIRECTIONS)
                {
                    var newPosition = position + direction;
                    if (newPosition == target)
                        return visited.Count;
                    if (!visited.Contains(newPosition) && IsPositionValid(newPosition, number))
                    {
                        var newVisited = visited.ToList();
                        newVisited.Add(newPosition);
                        queue.Enqueue(Tuple.Create(newPosition, newVisited));
                    }
                }
            }
            throw new Exception("Path not found");
        }

        static int Part2(int number)
        {
            var startPosition = new Complex(1, 1);
            var queue = new Queue<Tuple<Complex, List<Complex>>>();
            queue.Enqueue(Tuple.Create(startPosition, new List<Complex> { startPosition }));
            var allVisited = new HashSet<Complex>();
            while (queue.Any())
            {
                var (position, visited) = queue.Dequeue();
                if (visited.Count <= 50)
                {
                    foreach (var direction in DIRECTIONS)
                    {
                        var newPosition = position + direction;
                        if (!visited.Contains(newPosition) && IsPositionValid(newPosition, number))
                        {
                            allVisited.Add(newPosition);
                            var newVisited = visited.ToList();
                            newVisited.Add(newPosition);
                            queue.Enqueue(Tuple.Create(newPosition, newVisited));
                        }
                    }
                }
            }
            return allVisited.Count;
        }

        static int GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return int.Parse(File.ReadAllText(filePath).Trim());
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
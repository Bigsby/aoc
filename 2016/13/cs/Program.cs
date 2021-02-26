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
        static (int, int) Solve(int number)
        {
            var startPosition = new Complex(1, 1);
            var queue = new Queue<Tuple<Complex, List<Complex>>>();
            queue.Enqueue(Tuple.Create(startPosition, new List<Complex> { startPosition }));
            var allVisited = new HashSet<Complex>();
            allVisited.Add(startPosition);
            var target = new Complex(31, 39);
            var part1Result = 0;
            while (queue.Any() && part1Result == 0)
            {
                var (position, visited) = queue.Dequeue();
                foreach (var direction in DIRECTIONS)
                {
                    var newPosition = position + direction;
                    if (newPosition == target)
                        part1Result = visited.Count;
                    if (!visited.Contains(newPosition) && IsPositionValid(newPosition, number))
                    {
                        if (visited.Count <= 50)
                            allVisited.Add(newPosition);
                        var newVisited = visited.ToList();
                        newVisited.Add(newPosition);
                        queue.Enqueue(Tuple.Create(newPosition, newVisited));
                    }
                }
            }
            return (part1Result, allVisited.Count);
        }

        static int GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : int.Parse(File.ReadAllText(filePath).Trim());

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
using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = Tuple<IEnumerable<int>, IEnumerable<int>>;

    static class Program
    {
        static int Part1(Input puzzleInput)
        { 
            var left = new Queue<int>(puzzleInput.Item1.OrderBy(id => id));
            var right = new Queue<int>(puzzleInput.Item2.OrderBy(id => id));
            var distanceTotal = 0;
            while (left.Any())
                distanceTotal += Math.Abs(right.Dequeue() - left.Dequeue());
            return distanceTotal;
        }

        static int Part2(Input puzzleInput)
        {
            var (left, right) = puzzleInput;
            var similarityScore = 0;
            foreach (var id in left)
                similarityScore += id * right.Count(rightId => rightId == id);
            return similarityScore;
        }

        static (int, int) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath))
                throw new FileNotFoundException(filePath);
            var left = new List<int>();
            var right = new List<int>();
            foreach (var line in File.ReadAllLines(filePath))
            {
                var split = line.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);
                left.Add(int.Parse(split[0]));
                right.Add(int.Parse(split[1]));
            }
            return Tuple.Create(left.AsEnumerable(), right.AsEnumerable());
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

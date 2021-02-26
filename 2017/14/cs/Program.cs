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
        const int MARKS_COUNT = 256;

        static (int[] marks, int currentMark, int skip) RunLengths(int[] marks, IEnumerable<int> lengths, int currentMark, int skip)
        {
            foreach (var length in lengths)
            {
                var toReverse = new Stack<int>();
                var reverseMark = currentMark;
                foreach (var _ in Enumerable.Range(0, length))
                {
                    toReverse.Push(marks[reverseMark]);
                    reverseMark = reverseMark < MARKS_COUNT - 1 ? reverseMark + 1 : 0;
                }
                reverseMark = currentMark;
                foreach (var _ in Enumerable.Range(0, length))
                {
                    marks[reverseMark] = toReverse.Pop();
                    reverseMark = reverseMark < MARKS_COUNT - 1 ? reverseMark + 1 : 0;
                }
                foreach (var _ in Enumerable.Range(0, length + skip))
                    currentMark = currentMark < MARKS_COUNT - 1 ? currentMark + 1 : 0;
                skip++;
            }
            return (marks, currentMark, skip);
        }
        static void PrintList<T>(IEnumerable<T> list) => WriteLine("[ " + string.Join(",", list) + " ]");

        static int[] SUFFIX = new [] { 17, 31, 73, 47, 23 };
        static string Knothash(string key)
        {
            var lengths = key.Select(c => (int)c);
            lengths = lengths.Concat(SUFFIX);
            var marks = Enumerable.Range(0, MARKS_COUNT).ToArray();
            var currentMark = 0;
            var skip = 0;
            foreach (var _ in Enumerable.Range(0, 64))
            {
                (marks, currentMark, skip) = RunLengths(marks, lengths, currentMark, skip);
            }
            var denseHash = Enumerable.Range(0, 16)
                .Select(index => marks[new Range(index * 16, (index + 1) * 16)].Aggregate((soFar, mark) => soFar ^ mark));
            return string.Join("", denseHash.Select(knot => knot.ToString("x2")));
        }

        static string GetRowHashBinaryString(string key, int index)
        {
            var knotHash = Knothash(key + "-" + index.ToString());
            return string.Join("", Enumerable.Range(0, knotHash.Length / 2).Select(i => 
                Convert.ToString(Convert.ToInt32(knotHash[new Range(2 * i, 2 * (i + 1))], 16), 2).PadLeft(8, '0')));
        }

        static Complex[] DIRECTIONS = new [] { Complex.ImaginaryOne, 1, -Complex.ImaginaryOne, -1 };
        static void FindAdjacent(Complex point, HashSet<Complex> grid, HashSet<Complex> visited)
        {
            foreach (var direction in DIRECTIONS)
            {
                var adjacent = point + direction;
                if (grid.Contains(adjacent) && !visited.Contains(adjacent))
                {
                    visited.Add(adjacent);
                    FindAdjacent(adjacent, grid, visited);
                }
            }
        }

        static int Part2(string key)
        {
            var gridPoints = new HashSet<Complex>();
            foreach (var row in Enumerable.Range(0, 128))
                foreach (var (c, column) in GetRowHashBinaryString(key, row).Select((c, column) => (c, column)))
                    if (c == '1')
                        gridPoints.Add(new Complex(column, row));
            var region  = 0;
            while (gridPoints.Any())
            {
                region++;
                var point = gridPoints.Last();
                gridPoints.Remove(point);
                var visited = new HashSet<Complex>();
                visited.Add(point);
                FindAdjacent(point, gridPoints, visited);
                gridPoints.ExceptWith(visited);
            }
            return region;
        }

        static (int, int) Solve(string key)
            => (
                Enumerable.Range(0, 128).Sum(index => GetRowHashBinaryString(key, index).Count(c => c == '1')),
                Part2(key)
            );

        static string GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim();

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
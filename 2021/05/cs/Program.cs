using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    record Line(int x1, int y1, int x2, int y2);

    struct Point 
    {
        public Point(int x, int y)
        {
            X = x;
            Y = y;
        }
        public int X { get; }
        public int Y { get; }
        public override int GetHashCode() => HashCode.Combine(X, Y);
    }

    static class Program
    {
        static void AddToDiagram(IDictionary<Point, int> diagram, int x, int y)
        {
            var point = new Point(x, y);
            if (diagram.ContainsKey(point))
                diagram[point]++;
            else
                diagram[point] = 1;
        }

        static int GetCoveredCount(IEnumerable<Line> lines, bool diagonals)
        {
            var diagram = new Dictionary<Point, int>();
            foreach (var line in lines)
            {
                var (x1, y1, x2, y2) = line;
                if (x1 == x2)
                    for (var y = y1 < y2 ? y1 : y2; y < (y1 > y2 ? y1 : y2) + 1; y++)
                        AddToDiagram(diagram, x1, y);
                else if (y1 == y2)
                    for (var x = x1 < x2 ? x1 : x2; x < (x1 > x2 ? x1 : x2) + 1; x++)
                        AddToDiagram(diagram, x, y1);
                else if (diagonals)
                {
                    var xDirection = x2 > x1 ? 1 : -1;
                    var yDirection = y2 > y1 ? 1 : -1;
                    var count = Math.Abs(x2 - x1) + 1;
                    for (var xy = 0; xy < count; xy++)
                        AddToDiagram(diagram, x1 + xy * xDirection, y1 + xy * yDirection);
                }
            }
            return diagram.Values.Count(count => count > 1);
        }

        static (int, int) Solve(IEnumerable<Line> puzzleInput)
            => (GetCoveredCount(puzzleInput, false), GetCoveredCount(puzzleInput, true));

        static Regex lineRegex = new Regex(@"(?<x1>\d+),(?<y1>\d+) -> (?<x2>\d+),(?<y2>\d+)", RegexOptions.Compiled);
        static IEnumerable<Line> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var lines = new List<Line>();
            foreach (var line in File.ReadAllLines(filePath))
            {
                var lineMatch = lineRegex.Match(line);
                if (lineMatch.Success)
                {
                    lines.Add(new Line(
                        int.Parse(lineMatch.Groups["x1"].Value),
                        int.Parse(lineMatch.Groups["y1"].Value),
                        int.Parse(lineMatch.Groups["x2"].Value),
                        int.Parse(lineMatch.Groups["y2"].Value)
                    ));
                } else
                    throw new Exception($"Bad line: {line}");
            }
            return lines;
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

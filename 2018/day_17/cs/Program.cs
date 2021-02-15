using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    struct Coordinate
    {
        public int X { get; }
        public int Y { get; }

        public Coordinate(int x, int y)
        {
            X = x;
            Y = y;
        }

        public override bool Equals(object obj)
            => obj is Coordinate a && a.X == X && a.Y == Y;
        public override int GetHashCode()
            => base.GetHashCode();
        public static bool operator ==(Coordinate a, Coordinate b)
            => a.Equals(b);
        public static bool operator !=(Coordinate a, Coordinate b)
            => !a.Equals(b);
        public static Coordinate operator +(Coordinate a, Coordinate b)
            => new Coordinate(a.X + b.X, a.Y + b.Y);
        public static Coordinate operator -(Coordinate a, Coordinate b)
            => new Coordinate(a.X - b.X, a.Y - b.Y);
        public static Coordinate operator *(Coordinate a, Coordinate b)
            => new Coordinate(a.X * b.Y - a.X * b.Y, a.Y * b.X + a.X * b.Y);
        public static implicit operator Coordinate(int i)
            => new Coordinate(i, 0);
        public static Coordinate YOne = new Coordinate(0, 1);

        public void Deconstruct(out int x, out int y)
        {
            x = X;
            y = Y;
        }
        public Coordinate RotateLeft(int turns = 1)
            => this * new Coordinate(0, turns);
        public Coordinate RotateRight(int turns = 1)
            => this * new Coordinate(0, -turns);
        public override string ToString()
            => $"({X}, {Y})";
        
    }

    static class Program
    {
        static (int, int, int, int) GetEdges(IEnumerable<Coordinate> positions)
            => (
                positions.Min(p => p.X),
                positions.Max(p => p.X),
                positions.Min(p => p.Y),
                positions.Max(p => p.Y)
            );

        static void PrintArea(IEnumerable<Coordinate> clay, IEnumerable<Coordinate> flowing, IEnumerable<Coordinate> settled, Coordinate spring, bool all = false)
        {
            var (minX, maxX, minY, maxY) = GetEdges(clay.Concat(flowing).Concat(settled).Concat(new []{ spring }));
            var margins = 20;
            if (!all)
            {
                minX = (int)Math.Max(spring.X - margins * 2, minX);
                maxX = (int)Math.Min(spring.X + margins * 2, maxX);
                minY = (int)Math.Max(spring.Y - margins, minY);
                maxY = (int)Math.Min(spring.Y + margins, maxY);
            }
            for (var y = minY; y < maxY + 1; y++)
            {
                var line = string.Empty;
                for (var x = minX; x < maxX + 1; x++)
                {
                    var position = new Coordinate(x, y);
                    var c = ' ';
                    if (clay.Contains(position))
                        c = '#';
                    if (flowing.Contains(position))
                        c = '|';
                    if (settled.Contains(position))
                        c = '~';
                    if (position == spring)
                        c = '+';
                    line += c;
                }
                WriteLine(line);
            }
            WriteLine();
        }

        static (int, bool) FindEdge(Coordinate spring, int direction, IEnumerable<Coordinate> settled, IEnumerable<Coordinate> clay)
        {
            var offset = direction;
            while (true)
            {
                var current = spring + offset;
                if (clay.Contains(current))
                    return (offset - direction, false);
                var below = current + Coordinate.YOne;
                if (!clay.Contains(below) && !settled.Contains(below))
                    return (offset, true);
                offset += direction;
            }
        }

        static (int, int) Part1(IEnumerable<Coordinate> clay)
        {
            var maxY = (int)clay.Max(p => p.Y);
            var minY = (int)clay.Min(p => p.Y);
            var settled = new HashSet<Coordinate>();
            var flowing = new HashSet<Coordinate>();
            var dequeued = new HashSet<Coordinate>();
            var queue = new Stack<Coordinate>();
            queue.Push(new Coordinate(500, minY));
            while (queue.Any())
            {
                var spring = queue.Pop();
                if (dequeued.Contains(spring))
                    continue;
                var below = spring + Coordinate.YOne;
                if (flowing.Contains(below))
                    continue;
                flowing.Add(spring);
                while (below.Y <= maxY && !clay.Contains(below) && !settled.Contains(below))
                {
                    flowing.Add(below);
                    below += Coordinate.YOne;
                }
                if (clay.Contains(below) || settled.Contains(below))
                {
                    var (x, y) = (below.X, new Coordinate(0, below.Y - 1));
                    var (leftOffset, leftOverflown) = FindEdge(below - Coordinate.YOne, -1, settled, clay);
                    var (rightOffset, rightOverflown) = FindEdge(below - Coordinate.YOne, 1, settled, clay);
                    var isOverflown = leftOverflown || rightOverflown;
                    if (!isOverflown)
                        queue.Push(below - 2 * Coordinate.YOne);
                    for (var levelX = x + leftOffset; levelX < x + rightOffset + 1; levelX++)
                    {
                        var position = levelX + y;
                        if (isOverflown)
                            flowing.Add(position);
                        else
                        {
                            settled.Add(position);
                            flowing.Remove(position);
                            dequeued.Add(position);
                        }
                    }
                    if (leftOverflown)
                        queue.Push(x + leftOffset + y);
                    if (rightOverflown)
                        queue.Push(x + rightOffset + y);
                }
            }
            return (settled.Count + flowing.Count, settled.Count);
        }

        static Regex lineRegex = new Regex(@"^(?<sC>x|y)=(?<sV>\d+), (?:x|y)=(?<mS>\d+)..(?<mE>\d+)$", RegexOptions.Compiled);
        static IEnumerable<Coordinate> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).SelectMany(line => { 
                var match = lineRegex.Match(line);
                if (match.Success)
                {
                    var result = new List<Coordinate>();
                    var (sC, sV, mS, mE) = (
                        match.Groups["sC"].Value, 
                        int.Parse(match.Groups["sV"].Value), 
                        int.Parse(match.Groups["mS"].Value), 
                        int.Parse(match.Groups["mE"].Value));
                    if (sC == "x")
                        for (var y = mS; y < mE + 1; y++)
                            result.Add(new Coordinate(sV, y));
                    else
                        for (var x = mS; x < mE + 1; x++)
                            result.Add(new Coordinate(x, sV));
                    return result;
                }
                throw new Exception($"Base format '{line}'");
            });
        }

        static void Main(string[] args)
        {
            if (args.Length != 1) throw new Exception("Please, add input file path as parameter");

            var puzzleInput = GetInput(args[0]);
            var watch = Stopwatch.StartNew();
            var (part1Result, part2Result) = Part1(puzzleInput);
            watch.Stop();
            var middle = watch.ElapsedTicks;
            watch = Stopwatch.StartNew();
            watch.Stop();
            WriteLine($"P1: {part1Result}");
            WriteLine($"P2: {part2Result}");
            WriteLine();
            WriteLine($"P1 time: {(double)middle / 100 / TimeSpan.TicksPerSecond:f7}");
            WriteLine($"P2 time: {(double)watch.ElapsedTicks / 100 / TimeSpan.TicksPerSecond:f7}");
        }
    }
}

using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Input = HashSet<Complex>;

    static class Program
    {
        static int DropSand(Input initialRocks, bool infinite)
        {
            var rocks = new HashSet<Complex>(initialRocks);
            var bottom = (int)(rocks.Select(rock => rock.Imaginary).Max()) + (infinite ? 1 : 2);
            if (!infinite)
            {
                var rocksXs = rocks.Select(rock => rock.Real);
                var start = rocksXs.Min() - bottom;
                var end = rocksXs.Max() + bottom;
                for (var x = start; x < end; x++)
                    rocks.Add(new Complex(x, bottom));
            }
            var tap = new Complex(500, 0);
            var restedCount = 0;
            while (true)
            {
                var unit = tap;
                var isRested = false;
                while (true)
                {
                    var down = unit + Complex.ImaginaryOne;
                    var downLeft = down - 1;
                    var downRight = down + 1;
                    if (down.Imaginary == bottom)
                        break;
                    if (rocks.Contains(down) && rocks.Contains(downLeft) && rocks.Contains(downRight))
                    {
                        isRested = true;
                        break;
                    }
                    if (!rocks.Contains(down))
                        unit = down;
                    else if (!rocks.Contains(downLeft))
                        unit = downLeft;
                    else if (!rocks.Contains(downRight))
                        unit = downRight;
                }
                if (infinite && (unit.Imaginary == bottom || !isRested))
                    break;
                rocks.Add(unit);
                restedCount++;
                if (unit == tap)
                    break;
            }
            return restedCount;
        }

        static (int, int) Solve(Input rocks)
            => (DropSand(rocks, true), DropSand(rocks, false));

        static Complex ParsePoint(string text)
        {
            var split = text.Split(",");
            return new Complex(int.Parse(split[0]), int.Parse(split[1]));
        }

        static Complex GetDirection(Complex start, Complex end)
        {
            if (start.Real == end.Real)
                return end.Imaginary > start.Imaginary ? Complex.ImaginaryOne : -Complex.ImaginaryOne;
            return end.Real > start.Real ? Complex.One : -Complex.One;
        }

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var rocks = new HashSet<Complex>();
            foreach (var line in File.ReadAllLines(filePath))
            {
                var points = new Queue<Complex>(line.Split(" -> ").Select(point => ParsePoint(point)));
                var start = points.Dequeue();
                while (points.Any())
                {
                    var end = points.Dequeue();
                    var direction = GetDirection(start, end);
                    while (true)
                    {
                        rocks.Add(start);
                        if (start == end)
                            break;
                        start += direction;
                    }
                }
            }
            return rocks;
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

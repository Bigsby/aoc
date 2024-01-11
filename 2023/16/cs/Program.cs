using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Input = Dictionary<Complex, char>;

    static class Program
    {
        static int GetEnergizedCount(Input puzzleInput, (Complex, Complex) start)
        {
            var maxX = puzzleInput.Keys.Max(k => k.Real) + 1;
            var maxY = puzzleInput.Keys.Max(k => k.Imaginary) + 1;
            var energized = new HashSet<Complex>();
            var visited = new HashSet<(Complex, Complex)>();
            var beams = new Queue<(Complex, Complex)>();
            beams.Enqueue(start);
            while (beams.Any())
            {
                var (location, direction) = beams.Dequeue();
                energized.Add(location);
                var nextLocation = location + direction;
                if (nextLocation.Real < 0 || nextLocation.Real == maxX || nextLocation.Imaginary < 0 || nextLocation.Imaginary == maxY)
                    continue;
                if (!visited.Add((nextLocation, direction)))
                    continue;
                if (puzzleInput.TryGetValue(nextLocation, out var mirror))
                {
                    switch ((mirror, direction.Real, direction.Imaginary))
                    {
                        case ('-', 0, _):
                            beams.Enqueue((nextLocation, Complex.One));
                            beams.Enqueue((nextLocation, -Complex.One));
                            break;
                        case ('-', _, 0):
                            beams.Enqueue((nextLocation, direction));
                            break;
                        case ('|', _, 0):
                            beams.Enqueue((nextLocation, Complex.ImaginaryOne));
                            beams.Enqueue((nextLocation, -Complex.ImaginaryOne));
                            break;
                        case ('|', 0, _):
                            beams.Enqueue((nextLocation, direction));
                            break;
                        case ('/', _, 0):
                            beams.Enqueue((nextLocation, new Complex(0, -direction.Real)));
                            break;
                        case ('/', 0, _):
                            beams.Enqueue((nextLocation, new Complex(-direction.Imaginary, 0)));
                            break;
                        case ('\\', _, 0):
                            beams.Enqueue((nextLocation, new Complex(0, direction.Real)));
                            break;
                        case ('\\', 0, _):
                            beams.Enqueue((nextLocation, new Complex(direction.Imaginary, 0)));
                            break;
                    }
                }
                else
                    beams.Enqueue((nextLocation, direction));
            }
            return energized.Count - 1;
        }

        static int Part2(Input puzzleInput)
        {
            var result = 0;
            var maxX = puzzleInput.Keys.Max(k => k.Real) + 1;
            var maxY = puzzleInput.Keys.Max(k => k.Imaginary) + 1;
            for (var x = 0; x < maxX; x++)
            {
                result = Math.Max(result, GetEnergizedCount(puzzleInput, (new Complex(x, - 1), Complex.ImaginaryOne)));
                result = Math.Max(result, GetEnergizedCount(puzzleInput, (new Complex(x, maxY), -Complex.ImaginaryOne)));
            }
            for (var y = 0; y < maxY; y++)
            {
                result = Math.Max(result, GetEnergizedCount(puzzleInput, (new Complex(-1, y), Complex.One)));
                result = Math.Max(result, GetEnergizedCount(puzzleInput, (new Complex(maxX, y), -Complex.One)));
            }
            return result;
        }

        static (int, int) Solve(Input puzzleInput)
            => (GetEnergizedCount(puzzleInput, (-Complex.One, Complex.One)), Part2(puzzleInput));

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath))
                throw new FileNotFoundException(filePath);
            var result = new Dictionary<Complex, char>();
            var row = 0;
            foreach (var line in File.ReadAllLines(filePath))
            {
                var column = 0;
                foreach (var c in line.Trim())
                {
                    if (c != '.')
                        result[new Complex(column, row)] = c;
                    column++;
                }
                row++;
            }
            return result;
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

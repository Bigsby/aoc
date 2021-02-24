using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Tubes = List<Complex>;
    using Letters = Dictionary<Complex, char>;

    static class Program
    {
        static (string letters, int steps) FollowPath((Tubes, Letters, Complex) data)
        {
            var (tubes, letters, currentPosition) = data;
            var path = string.Empty;
            var direction = Complex.ImaginaryOne;
            var steps = 0;
            while (true)
            {
                steps++;
                if (letters.ContainsKey(currentPosition))
                    path += letters[currentPosition];
                if (tubes.Contains(currentPosition + direction))
                    currentPosition += direction;
                else if (tubes.Contains(currentPosition + direction * Complex.ImaginaryOne))
                {
                    direction *= Complex.ImaginaryOne;
                    currentPosition += direction;
                }
                else if (tubes.Contains(currentPosition + direction * -Complex.ImaginaryOne))
                {
                    direction *= -Complex.ImaginaryOne;
                    currentPosition += direction;
                }
                else
                    break;
            }
            return (path, steps);
        }

        static string Part1((Tubes, Letters, Complex) data) => FollowPath(data).letters;

        static int Part2((Tubes, Letters, Complex) data) => FollowPath(data).steps;

        static char[] TUBES = new [] { '|', '+', '-' };
        static (Tubes, Letters, Complex) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var tubes = new Tubes();
            var letters = new Letters();
            var start = Complex.Zero;
            foreach (var (line, y) in File.ReadLines(filePath).Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                {
                    var position = new Complex(x, y);
                    if (TUBES.Contains(c))
                    {
                        tubes.Add(position);
                        if (y == 0)
                            start = position;
                    }
                    if (c >= 'A' && c <= 'Z')
                    {
                        letters[position] = c;
                        tubes.Add(position);
                    }
                }
            return (tubes, letters, start);
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

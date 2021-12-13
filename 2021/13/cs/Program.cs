using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    record struct Folding(char direction, int coordinate);

    static class Program
    {
        const int SCREEN_WIDTH = 40;
        const int SCREEN_HEIGTH = 6;
        const int CHARACTER_WIDTH = 5;
        static IDictionary<int, char> LETTERS = new Dictionary<int, char> {
            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b11110 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'A' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b11100 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b11100 << CHARACTER_WIDTH * 5), 'B' },

            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'C' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b11100 << CHARACTER_WIDTH * 5), 'D' },

            {   (0b11110 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b11100 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b11110 << CHARACTER_WIDTH * 5), 'E' },

            {   (0b11110 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b11100 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b10000 << CHARACTER_WIDTH * 5), 'F' },

            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b10110 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01110 << CHARACTER_WIDTH * 5), 'G' },

            {   (0b10010 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b11110 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'H' },

            {   (0b01110 << CHARACTER_WIDTH * 0) +
                (0b00100 << CHARACTER_WIDTH * 1) +
                (0b00100 << CHARACTER_WIDTH * 2) +
                (0b00100 << CHARACTER_WIDTH * 3) +
                (0b00100 << CHARACTER_WIDTH * 4) +
                (0b01110 << CHARACTER_WIDTH * 5), 'I' },

            {   (0b00110 << CHARACTER_WIDTH * 0) +
                (0b00010 << CHARACTER_WIDTH * 1) +
                (0b00010 << CHARACTER_WIDTH * 2) +
                (0b00010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'J' },

            {   (0b10010 << CHARACTER_WIDTH * 0) +
                (0b10100 << CHARACTER_WIDTH * 1) +
                (0b11000 << CHARACTER_WIDTH * 2) +
                (0b10100 << CHARACTER_WIDTH * 3) +
                (0b10100 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'K' },

            {   (0b10000 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b11110 << CHARACTER_WIDTH * 5), 'L' },

            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'O' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b11100 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b10000 << CHARACTER_WIDTH * 5), 'P' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b11100 << CHARACTER_WIDTH * 3) +
                (0b10100 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'R' },

            {   (0b01110 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b01100 << CHARACTER_WIDTH * 3) +
                (0b00010 << CHARACTER_WIDTH * 4) +
                (0b11100 << CHARACTER_WIDTH * 5), 'S' },

            {   (0b10010 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'U' },

            {   (0b10001 << CHARACTER_WIDTH * 0) +
                (0b10001 << CHARACTER_WIDTH * 1) +
                (0b01010 << CHARACTER_WIDTH * 2) +
                (0b00100 << CHARACTER_WIDTH * 3) +
                (0b00100 << CHARACTER_WIDTH * 4) +
                (0b00100 << CHARACTER_WIDTH * 5), 'Y' },

            {   (0b11110 << CHARACTER_WIDTH * 0) +
                (0b00010 << CHARACTER_WIDTH * 1) +
                (0b00100 << CHARACTER_WIDTH * 2) +
                (0b01000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b11110 << CHARACTER_WIDTH * 5), 'Z' }
        };

        static char GetCharacterInScreen(IEnumerable<Complex> points, int index, int width, int height)
        {
            var screenValue = Enumerable.Range(0, height).SelectMany(y => Enumerable.Range(0, width).Select(x => (x, y)))
                .Where(pair => points.Contains(new Complex(width * index + pair.x, pair.y)))
                .Sum(pair => (int)Math.Pow(2, width - 1 - pair.x) << (pair.y * width));
            return LETTERS[screenValue];
        }

        static IEnumerable<Complex> Fold(IEnumerable<Complex> points, Folding folding)
        {
            Func<Complex, double> includeFunc = folding.direction == 'x' ?
                (point => point.Real)
                :
                (point => point.Imaginary);
            Func<Complex, int, Complex> newPointFunc = folding.direction == 'x' ?
                ((point, coordinate) => new Complex(2 * coordinate - point.Real, point.Imaginary))
                :
                ((point, coordinate) => new Complex(point.Real, 2 * coordinate - point.Imaginary));
            var newPoints = new List<Complex>();
            foreach (var point in points)
            {
                var newPoint = includeFunc(point) < folding.coordinate ? point : newPointFunc(point, folding.coordinate);
                if (!newPoints.Contains(newPoint))
                    newPoints.Add(newPoint);
            }
            return newPoints;
        }

        static (int, string) Solve((IEnumerable<Complex>,IEnumerable<Folding>) puzzleInput)
        {
            var (points, foldings) = puzzleInput;
            int part1 = 0;
            foreach (var folding in foldings)
            {
                points = Fold(points, folding);
                if (part1 == 0)
                    part1 = points.Count();
            }

            return (
                part1, 
                new string(Enumerable.Range(0, SCREEN_WIDTH / CHARACTER_WIDTH)
                    .Select(index => 
                        GetCharacterInScreen(points, index, CHARACTER_WIDTH, SCREEN_HEIGTH)
                    ).ToArray())
            );
        }

        static (IEnumerable<Complex>,IEnumerable<Folding>) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);

            var points = new List<Complex>();
            var foldings = new List<Folding>();
            var folding = false;
            foreach (var line in File.ReadAllLines(filePath))
            {
                if (String.IsNullOrEmpty(line))
                {
                    folding = true;
                    continue;
                }
                if (folding)
                {
                    var relevant = line.Split(" ")[2].Split("=");
                    foldings.Add(new Folding(relevant[0][0], int.Parse(relevant[1])));
                }
                else
                {
                    var split = line.Split(",");
                    points.Add(new Complex(int.Parse(split[0]), int.Parse(split[1])));
                }
            }
            return (points, foldings);
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

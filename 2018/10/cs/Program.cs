using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Numerics;

namespace AoC
{
    using PointPairs = IEnumerable<(Complex position, Complex velocity)>;

    class Program
    {
        const int CHARACTER_WIDTH = 6;
        const int CHARACTER_PADDING = 2;
        const int CHARACTER_HEIGHT = 10;
        static Dictionary<long, char> LETTERS = new Dictionary<long, char> {
            {
                (0b001100L << CHARACTER_WIDTH * 0) +
                (0b010010L << CHARACTER_WIDTH * 1) +
                (0b100001L << CHARACTER_WIDTH * 2) +
                (0b100001L << CHARACTER_WIDTH * 3) +
                (0b100001L << CHARACTER_WIDTH * 4) +
                (0b111111L << CHARACTER_WIDTH * 5) +
                (0b100001L << CHARACTER_WIDTH * 6) +
                (0b100001L << CHARACTER_WIDTH * 7) +
                (0b100001L << CHARACTER_WIDTH * 8) +
                (0b100001L << CHARACTER_WIDTH * 9), 'A' },
            {
                (0b111110L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100001L << CHARACTER_WIDTH * 2) +
                (0b100001L << CHARACTER_WIDTH * 3) +
                (0b111110L << CHARACTER_WIDTH * 4) +
                (0b100001L << CHARACTER_WIDTH * 5) +
                (0b100001L << CHARACTER_WIDTH * 6) +
                (0b100001L << CHARACTER_WIDTH * 7) +
                (0b100001L << CHARACTER_WIDTH * 8) +
                (0b111110L << CHARACTER_WIDTH * 9), 'B' },
            {
                (0b011110L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100000L << CHARACTER_WIDTH * 2) +
                (0b100000L << CHARACTER_WIDTH * 3) +
                (0b100000L << CHARACTER_WIDTH * 4) +
                (0b100000L << CHARACTER_WIDTH * 5) +
                (0b100000L << CHARACTER_WIDTH * 6) +
                (0b100000L << CHARACTER_WIDTH * 7) +
                (0b100001L << CHARACTER_WIDTH * 8) +
                (0b011110L << CHARACTER_WIDTH * 9), 'C' },
            {
                (0b111110L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100001L << CHARACTER_WIDTH * 2) +
                (0b100001L << CHARACTER_WIDTH * 3) +
                (0b100001L << CHARACTER_WIDTH * 4) +
                (0b100001L << CHARACTER_WIDTH * 5) +
                (0b100001L << CHARACTER_WIDTH * 6) +
                (0b100001L << CHARACTER_WIDTH * 7) +
                (0b100001L << CHARACTER_WIDTH * 8) +
                (0b111110L << CHARACTER_WIDTH * 9), 'D' },
            {
                (0b111111L << CHARACTER_WIDTH * 0) +
                (0b100000L << CHARACTER_WIDTH * 1) +
                (0b100000L << CHARACTER_WIDTH * 2) +
                (0b100000L << CHARACTER_WIDTH * 3) +
                (0b111110L << CHARACTER_WIDTH * 4) +
                (0b100000L << CHARACTER_WIDTH * 5) +
                (0b100000L << CHARACTER_WIDTH * 6) +
                (0b100000L << CHARACTER_WIDTH * 7) +
                (0b100000L << CHARACTER_WIDTH * 8) +
                (0b111111L << CHARACTER_WIDTH * 9), 'E' },
            {
                (0b111111L << CHARACTER_WIDTH * 0) +
                (0b100000L << CHARACTER_WIDTH * 1) +
                (0b100000L << CHARACTER_WIDTH * 2) +
                (0b100000L << CHARACTER_WIDTH * 3) +
                (0b111110L << CHARACTER_WIDTH * 4) +
                (0b100000L << CHARACTER_WIDTH * 5) +
                (0b100000L << CHARACTER_WIDTH * 6) +
                (0b100000L << CHARACTER_WIDTH * 7) +
                (0b100000L << CHARACTER_WIDTH * 8) +
                (0b100000L << CHARACTER_WIDTH * 9), 'F' },
            {
                (0b011110L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100000L << CHARACTER_WIDTH * 2) +
                (0b100000L << CHARACTER_WIDTH * 3) +
                (0b100000L << CHARACTER_WIDTH * 4) +
                (0b100111L << CHARACTER_WIDTH * 5) +
                (0b100001L << CHARACTER_WIDTH * 6) +
                (0b100001L << CHARACTER_WIDTH * 7) +
                (0b100011L << CHARACTER_WIDTH * 8) +
                (0b011101L << CHARACTER_WIDTH * 9), 'G' },
            {
                (0b100001L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100001L << CHARACTER_WIDTH * 2) +
                (0b100001L << CHARACTER_WIDTH * 3) +
                (0b111111L << CHARACTER_WIDTH * 4) +
                (0b100001L << CHARACTER_WIDTH * 5) +
                (0b100001L << CHARACTER_WIDTH * 6) +
                (0b100001L << CHARACTER_WIDTH * 7) +
                (0b100001L << CHARACTER_WIDTH * 8) +
                (0b100001L << CHARACTER_WIDTH * 9), 'H' },
            {
                (0b111000L << CHARACTER_WIDTH * 0) +
                (0b010000L << CHARACTER_WIDTH * 1) +
                (0b010000L << CHARACTER_WIDTH * 2) +
                (0b010000L << CHARACTER_WIDTH * 3) +
                (0b010000L << CHARACTER_WIDTH * 4) +
                (0b010000L << CHARACTER_WIDTH * 5) +
                (0b010000L << CHARACTER_WIDTH * 6) +
                (0b010000L << CHARACTER_WIDTH * 7) +
                (0b010000L << CHARACTER_WIDTH * 8) +
                (0b111000L << CHARACTER_WIDTH * 9), 'I' }, // Not sure
            {
                (0b000111L << CHARACTER_WIDTH * 0) +
                (0b000010L << CHARACTER_WIDTH * 1) +
                (0b000010L << CHARACTER_WIDTH * 2) +
                (0b000010L << CHARACTER_WIDTH * 3) +
                (0b000010L << CHARACTER_WIDTH * 4) +
                (0b000010L << CHARACTER_WIDTH * 5) +
                (0b000010L << CHARACTER_WIDTH * 6) +
                (0b100010L << CHARACTER_WIDTH * 7) +
                (0b100010L << CHARACTER_WIDTH * 8) +
                (0b011100L << CHARACTER_WIDTH * 9), 'J' },
            {
                (0b100001L << CHARACTER_WIDTH * 0) +
                (0b100010L << CHARACTER_WIDTH * 1) +
                (0b100100L << CHARACTER_WIDTH * 2) +
                (0b101000L << CHARACTER_WIDTH * 3) +
                (0b110000L << CHARACTER_WIDTH * 4) +
                (0b110000L << CHARACTER_WIDTH * 5) +
                (0b101000L << CHARACTER_WIDTH * 6) +
                (0b100100L << CHARACTER_WIDTH * 7) +
                (0b100010L << CHARACTER_WIDTH * 8) +
                (0b100001L << CHARACTER_WIDTH * 9), 'K' },
            {
                (0b100000L << CHARACTER_WIDTH * 0) +
                (0b100000L << CHARACTER_WIDTH * 1) +
                (0b100000L << CHARACTER_WIDTH * 2) +
                (0b100000L << CHARACTER_WIDTH * 3) +
                (0b100000L << CHARACTER_WIDTH * 4) +
                (0b100000L << CHARACTER_WIDTH * 5) +
                (0b100000L << CHARACTER_WIDTH * 6) +
                (0b100000L << CHARACTER_WIDTH * 7) +
                (0b100000L << CHARACTER_WIDTH * 8) +
                (0b111111L << CHARACTER_WIDTH * 9), 'L' },
            {
                (0b100001L << CHARACTER_WIDTH * 0) +
                (0b110011L << CHARACTER_WIDTH * 1) +
                (0b110011L << CHARACTER_WIDTH * 2) +
                (0b101101L << CHARACTER_WIDTH * 3) +
                (0b100001L << CHARACTER_WIDTH * 4) +
                (0b100001L << CHARACTER_WIDTH * 5) +
                (0b100001L << CHARACTER_WIDTH * 6) +
                (0b100001L << CHARACTER_WIDTH * 7) +
                (0b100001L << CHARACTER_WIDTH * 8) +
                (0b100001L << CHARACTER_WIDTH * 9), 'M' }, // Not sure
            {
                (0b100001L << CHARACTER_WIDTH * 0) +
                (0b110001L << CHARACTER_WIDTH * 1) +
                (0b110001L << CHARACTER_WIDTH * 2) +
                (0b101001L << CHARACTER_WIDTH * 3) +
                (0b101001L << CHARACTER_WIDTH * 4) +
                (0b100101L << CHARACTER_WIDTH * 5) +
                (0b100101L << CHARACTER_WIDTH * 6) +
                (0b100011L << CHARACTER_WIDTH * 7) +
                (0b100011L << CHARACTER_WIDTH * 8) +
                (0b100001L << CHARACTER_WIDTH * 9), 'N' },
            {
                (0b011110L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100001L << CHARACTER_WIDTH * 2) +
                (0b100001L << CHARACTER_WIDTH * 3) +
                (0b100001L << CHARACTER_WIDTH * 4) +
                (0b100001L << CHARACTER_WIDTH * 5) +
                (0b100001L << CHARACTER_WIDTH * 6) +
                (0b100001L << CHARACTER_WIDTH * 7) +
                (0b100001L << CHARACTER_WIDTH * 8) +
                (0b011110L << CHARACTER_WIDTH * 9), 'O' },
            {
                (0b111110L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100001L << CHARACTER_WIDTH * 2) +
                (0b100001L << CHARACTER_WIDTH * 3) +
                (0b111110L << CHARACTER_WIDTH * 4) +
                (0b100000L << CHARACTER_WIDTH * 5) +
                (0b100000L << CHARACTER_WIDTH * 6) +
                (0b100000L << CHARACTER_WIDTH * 7) +
                (0b100000L << CHARACTER_WIDTH * 8) +
                (0b100000L << CHARACTER_WIDTH * 9), 'P' },
            {
                (0b011110L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100001L << CHARACTER_WIDTH * 2) +
                (0b100001L << CHARACTER_WIDTH * 3) +
                (0b100001L << CHARACTER_WIDTH * 4) +
                (0b100001L << CHARACTER_WIDTH * 5) +
                (0b100001L << CHARACTER_WIDTH * 6) +
                (0b100101L << CHARACTER_WIDTH * 7) +
                (0b100110L << CHARACTER_WIDTH * 8) +
                (0b011001L << CHARACTER_WIDTH * 9), 'Q' }, // Not sure
            {
                (0b111110L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100001L << CHARACTER_WIDTH * 2) +
                (0b100001L << CHARACTER_WIDTH * 3) +
                (0b111110L << CHARACTER_WIDTH * 4) +
                (0b100100L << CHARACTER_WIDTH * 5) +
                (0b100010L << CHARACTER_WIDTH * 6) +
                (0b100010L << CHARACTER_WIDTH * 7) +
                (0b100001L << CHARACTER_WIDTH * 8) +
                (0b100001L << CHARACTER_WIDTH * 9), 'R' },
            {
                (0b011110L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100000L << CHARACTER_WIDTH * 2) +
                (0b100000L << CHARACTER_WIDTH * 3) +
                (0b011110L << CHARACTER_WIDTH * 4) +
                (0b000001L << CHARACTER_WIDTH * 5) +
                (0b000001L << CHARACTER_WIDTH * 6) +
                (0b000001L << CHARACTER_WIDTH * 7) +
                (0b100001L << CHARACTER_WIDTH * 8) +
                (0b011110L << CHARACTER_WIDTH * 9), 'S' },
            {
                (0b111110L << CHARACTER_WIDTH * 0) +
                (0b001000L << CHARACTER_WIDTH * 1) +
                (0b001000L << CHARACTER_WIDTH * 2) +
                (0b001000L << CHARACTER_WIDTH * 3) +
                (0b001000L << CHARACTER_WIDTH * 4) +
                (0b001000L << CHARACTER_WIDTH * 5) +
                (0b001000L << CHARACTER_WIDTH * 6) +
                (0b001000L << CHARACTER_WIDTH * 7) +
                (0b001000L << CHARACTER_WIDTH * 8) +
                (0b001000L << CHARACTER_WIDTH * 9), 'T' }, // Not sure
            {
                (0b100001L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100001L << CHARACTER_WIDTH * 2) +
                (0b100001L << CHARACTER_WIDTH * 3) +
                (0b100001L << CHARACTER_WIDTH * 4) +
                (0b100001L << CHARACTER_WIDTH * 5) +
                (0b100001L << CHARACTER_WIDTH * 6) +
                (0b100001L << CHARACTER_WIDTH * 7) +
                (0b100001L << CHARACTER_WIDTH * 8) +
                (0b011110L << CHARACTER_WIDTH * 9), 'U' },
            {
                (0b100001L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100001L << CHARACTER_WIDTH * 2) +
                (0b100001L << CHARACTER_WIDTH * 3) +
                (0b100001L << CHARACTER_WIDTH * 4) +
                (0b100001L << CHARACTER_WIDTH * 5) +
                (0b100001L << CHARACTER_WIDTH * 6) +
                (0b010010L << CHARACTER_WIDTH * 7) +
                (0b010010L << CHARACTER_WIDTH * 8) +
                (0b001100L << CHARACTER_WIDTH * 9), 'V' }, // Not sure
            {
                (0b100001L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b100001L << CHARACTER_WIDTH * 2) +
                (0b100001L << CHARACTER_WIDTH * 3) +
                (0b100001L << CHARACTER_WIDTH * 4) +
                (0b100001L << CHARACTER_WIDTH * 5) +
                (0b101101L << CHARACTER_WIDTH * 6) +
                (0b101101L << CHARACTER_WIDTH * 7) +
                (0b110011L << CHARACTER_WIDTH * 8) +
                (0b100001L << CHARACTER_WIDTH * 9), 'W' }, // Not sure
            {
                (0b100001L << CHARACTER_WIDTH * 0) +
                (0b100001L << CHARACTER_WIDTH * 1) +
                (0b010010L << CHARACTER_WIDTH * 2) +
                (0b010010L << CHARACTER_WIDTH * 3) +
                (0b001100L << CHARACTER_WIDTH * 4) +
                (0b001100L << CHARACTER_WIDTH * 5) +
                (0b010010L << CHARACTER_WIDTH * 6) +
                (0b010010L << CHARACTER_WIDTH * 7) +
                (0b100001L << CHARACTER_WIDTH * 8) +
                (0b100001L << CHARACTER_WIDTH * 9), 'X' },
            {
                (0b100010L << CHARACTER_WIDTH * 0) +
                (0b100010L << CHARACTER_WIDTH * 1) +
                (0b010100L << CHARACTER_WIDTH * 2) +
                (0b010100L << CHARACTER_WIDTH * 3) +
                (0b001000L << CHARACTER_WIDTH * 4) +
                (0b001000L << CHARACTER_WIDTH * 5) +
                (0b001000L << CHARACTER_WIDTH * 6) +
                (0b001000L << CHARACTER_WIDTH * 7) +
                (0b001000L << CHARACTER_WIDTH * 8) +
                (0b001000L << CHARACTER_WIDTH * 9), 'Y' }, // Not sure
            {
                (0b111111L << CHARACTER_WIDTH * 0) +
                (0b000001L << CHARACTER_WIDTH * 1) +
                (0b000001L << CHARACTER_WIDTH * 2) +
                (0b000010L << CHARACTER_WIDTH * 3) +
                (0b000100L << CHARACTER_WIDTH * 4) +
                (0b001000L << CHARACTER_WIDTH * 5) +
                (0b010000L << CHARACTER_WIDTH * 6) +
                (0b100000L << CHARACTER_WIDTH * 7) +
                (0b100000L << CHARACTER_WIDTH * 8) +
                (0b111111L << CHARACTER_WIDTH * 9), 'Z' }
        };

        static void PrintPoints(PointPairs pointPairs)
        {
            var (_, minX, maxX, minY, maxY) = GetDimensions(pointPairs);
            if (maxY - minY > 50)
                return;
            var points = pointPairs.Select(pair => pair.position);
            for (var y = minY; y <= maxY; y++)
            {
                for (var x = minX; x <= maxX; x++)
                {
                    var c = ".";
                    if (points.Contains(new Complex(x, y)))
                        c = "#";
                    Write(c);
                }
                WriteLine();
            }
            WriteLine();
        }

        static ((int width, int height), int minX, int maxX, int minY, int maxY) GetDimensions(PointPairs points)
        {
            var positions = points.Select(pair => pair.position);
            var minX = (int)positions.Min(position => position.Real);
            var maxX = (int)positions.Max(position => position.Real);
            var minY = (int)positions.Min(position => position.Imaginary);
            var maxY = (int)positions.Max(position => position.Imaginary);
            return ((Math.Abs(maxX - minX + 1), Math.Abs(maxY - minY + 1)), minX, maxX, minY, maxY);
        }

        static PointPairs GetNextState(PointPairs points)
        {
            var result = new List<(Complex position, Complex velocity)>();
            foreach (var pair in points)
                result.Add((pair.position + pair.velocity, pair.velocity));
            return result;
        }

        static char GetCharacter(int minX, int minY, int index, int characterWidth, IEnumerable<Complex> points)
        {
            var screenValue = Enumerable.Range(0, CHARACTER_HEIGHT).SelectMany(y => Enumerable.Range(0, CHARACTER_WIDTH).Select(x => (x, y)))
                .Where(pair => points.Contains(new Complex(characterWidth * index + pair.x + minX, pair.y + minY)))
                .Sum(pair => (long)Math.Pow(2, CHARACTER_WIDTH - 1 - pair.x) << (pair.y * CHARACTER_WIDTH));
            return LETTERS[screenValue];
        }

        static (bool success, string message) GetMessage(PointPairs pointPairs)
        {
            var points = pointPairs.Select(point => point.position);
            var ((width, _), minX, _, minY, _) = GetDimensions(pointPairs);
            var characterWidth = CHARACTER_WIDTH + CHARACTER_PADDING;
            try
            {
                return (true,
                    string.Join("",
                        Enumerable.Range(0, (width / characterWidth) + 1)
                            .Select(index => GetCharacter(minX, minY, index, characterWidth, points))));
            }
            catch
            {
                return (false, string.Empty);
            }
        }

        static (string, int) Solve(PointPairs pointPairs)
        {
            var interations = 0;
            while (true)
            {
                var ((_, height), _, _, _, _) = GetDimensions(pointPairs);
                if (height == CHARACTER_HEIGHT)
                {
                    var result = GetMessage(pointPairs);
                    if (result.success)
                        return (result.message, interations);
                }
                pointPairs = GetNextState(pointPairs);
                interations++;
            }
        }

        static Regex lineRegex = new Regex(@"^position=<\s?(?<positionX>-?\d+),\s+(?<positionY>-?\d+)>\svelocity=<\s?(?<velocityX>-?\d+),\s+?(?<velocityY>-?\d+)>$", RegexOptions.Compiled);
        static PointPairs GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line =>
            {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return (
                        new Complex(int.Parse(match.Groups["positionX"].Value), int.Parse(match.Groups["positionY"].Value)),
                        new Complex(int.Parse(match.Groups["velocityX"].Value), int.Parse(match.Groups["velocityY"].Value))
                    );
                throw new Exception($"Bad format '{line}'");
            });

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
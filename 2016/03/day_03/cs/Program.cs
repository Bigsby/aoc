using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        static bool IsPossibleTriangle(int sideA, int sideB, int sideC)
            => sideA < (sideB + sideC) &&
            sideB < (sideA + sideC) &&
            sideC < (sideA + sideB);

        static int Part1(int[][] triangleSides)
        {
            return triangleSides.Count(sides => IsPossibleTriangle(sides[0], sides[1], sides[2]));
        }

        static int Part2(int[][] triangleSides)
        {
            return Enumerable.Range(0, triangleSides.Length).Count(index =>
                IsPossibleTriangle(
                    triangleSides[(index / 3) * 3][index % 3],
                    triangleSides[(index / 3) * 3 + 1][index % 3],
                    triangleSides[(index / 3) * 3 + 2][index % 3]));
        }

        static Regex lineRegex = new Regex(@"(\d+)", RegexOptions.Compiled);
        static int[][] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath)
                .Select(line => lineRegex.Matches(line).Select(match => int.Parse(match.Groups[1].Value)).ToArray()).ToArray();
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
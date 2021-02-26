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

        static (int, int) Solve(int[][] triangleSides)
            => (
                triangleSides.Count(sides => IsPossibleTriangle(sides[0], sides[1], sides[2])),
                Enumerable.Range(0, triangleSides.Length).Count(index =>
                    IsPossibleTriangle(
                        triangleSides[(index / 3) * 3][index % 3],
                        triangleSides[(index / 3) * 3 + 1][index % 3],
                        triangleSides[(index / 3) * 3 + 2][index % 3]))
            );

        static Regex lineRegex = new Regex(@"(\d+)", RegexOptions.Compiled);
        static int[][] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath)
                .Select(line => lineRegex.Matches(line).Select(match => int.Parse(match.Groups[1].Value)).ToArray()).ToArray();

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
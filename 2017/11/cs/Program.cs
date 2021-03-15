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
    class Program
    {
        static Dictionary<string, Complex> DIRECTIONS = new Dictionary<string, Complex> {
            { "s", new Complex(0, 1) },
            { "se", new Complex(1, 0) },
            { "sw", new Complex( -1, 1) },
            { "ne", new Complex(1, -1) },
            { "nw", new Complex(-1, 0) },
            { "n",  new Complex(0, -1) }
        };

        static int GetHexManhatanDistance(Complex position)
            => (position.Real > 0) ^ (position.Imaginary > 0) ?
                (int)Math.Max(Math.Abs(position.Real), Math.Abs(position.Imaginary))
                : (int)(Math.Abs(position.Real) + Math.Abs(position.Imaginary));

        static (int, int) Solve(IEnumerable<string> instructions)
        {
            var furthest = 0;
            Complex currentHex = 0;
            foreach (var instrucion in instructions)
            {
                currentHex += DIRECTIONS[instrucion];
                furthest = Math.Max(furthest, GetHexManhatanDistance(currentHex));
            }
            return (GetHexManhatanDistance(currentHex), furthest);
        }

        static Regex instructionRegex = new Regex(@"ne|nw|n|sw|se|s", RegexOptions.Compiled);
        static IEnumerable<string> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : instructionRegex.Matches(File.ReadAllText(filePath)).Select(match => match.Groups[0].Value);


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
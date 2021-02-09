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
            { "s", Complex.ImaginaryOne },
            { "se", 1 },
            { "sw", new Complex( -1, 1) },
            { "ne", new Complex(1, -1) },
            { "nw", -1 },
            { "n", -Complex.ImaginaryOne }
        };

        static int GetHexManhatanDistance(Complex position)
        {
            if ((position.Real > 0) ^ (position.Imaginary > 0))
                return (int)(Math.Max(Math.Abs(position.Real), Math.Abs(position.Imaginary)));
            return (int)(Math.Abs(position.Real) + Math.Abs(position.Imaginary));
        }

        static int Part1(IEnumerable<string> instructions)
            => GetHexManhatanDistance(instructions.Aggregate(Complex.Zero, (current, instruction) => current + DIRECTIONS[instruction]));

        static int Part2(IEnumerable<string> instructions)
        {

            var furthest = 0;
            Complex currentHex = 0;
            foreach (var instrucion in instructions)
            {
                currentHex += DIRECTIONS[instrucion];
                furthest = Math.Max(furthest, GetHexManhatanDistance(currentHex));
            }
            return furthest;
        }

        static Regex instructionRegex = new Regex(@"ne|nw|n|sw|se|s", RegexOptions.Compiled);
        static IEnumerable<string> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return instructionRegex.Matches(File.ReadAllText(filePath)).Select(match => match.Groups[0].Value);
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
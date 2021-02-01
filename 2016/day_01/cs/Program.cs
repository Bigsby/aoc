using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Numerics;

namespace AoC
{
    struct Instruction
    {
        public Instruction(char direction, int distance)
        {
            Direction = direction;
            Distance = distance;
        }

        public char Direction { get; }
        public int Distance { get; }
        public override string ToString()
        {
            return $"{Direction}{Distance}";
        }
    }

    class Program
    {
        static Complex GetNewHeading(Complex currentHeading, char direction)
            => currentHeading * (direction == 'L' ? Complex.ImaginaryOne : -Complex.ImaginaryOne);

        static int GetManhatanDistance(Complex position)
            => (int)(Math.Abs(position.Real) + Math.Abs(position.Imaginary));

        static int Part1(IEnumerable<Instruction> instructions)
        {
            var currentPosition = Complex.Zero;
            var currentHeading = Complex.ImaginaryOne;
            foreach (var instruction in instructions)
            {
                currentHeading = GetNewHeading(currentHeading, instruction.Direction);
                currentPosition += currentHeading * new Complex(instruction.Distance, 0);
            }
            return GetManhatanDistance(currentPosition);
        }

        static int Part2(IEnumerable<Instruction> instructions)
        {   
            var currentPosition = Complex.Zero;
            var currentHeading = Complex.ImaginaryOne;
            var visitedPositions = new List<Complex>();
            foreach (var instruction in instructions)
            {
                currentHeading = GetNewHeading(currentHeading, instruction.Direction);
                for (var i = 0; i < instruction.Distance; i++)
                {
                    currentPosition += currentHeading;
                    if (visitedPositions.Contains(currentPosition))
                    {
                        return GetManhatanDistance(currentPosition);
                    }
                    else
                    {
                        visitedPositions.Add(currentPosition);
                    }
                }
            }
            throw new Exception("Never returned to previous locations");
        }

        static Regex instructionRegex = new Regex(@"(?<direction>L|R)(?<distance>\d+)", RegexOptions.Compiled);
        static IEnumerable<Instruction> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);

            foreach (Match match in instructionRegex.Matches(File.ReadAllText(filePath)))
            {
                yield return new Instruction(match.Groups["direction"].Value[0], int.Parse(match.Groups["distance"].Value));
            }
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
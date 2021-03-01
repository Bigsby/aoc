using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.Numerics;

namespace AoC
{
    record Instruction(char direction, int distance);

    class Program
    {
        static Complex GetNewHeading(Complex heading, char direction)
            => heading * (direction == 'L' ? Complex.ImaginaryOne : -Complex.ImaginaryOne);

        static int GetManhatanDistance(Complex position)
            => (int)(Math.Abs(position.Real) + Math.Abs(position.Imaginary));

        static (int, int) Solve(IEnumerable<Instruction> instructions)
        {
            Complex position = 0;
            var heading = Complex.ImaginaryOne;
            var visited = new List<Complex>();
            var part2 = 0;
            foreach (var instruction in instructions)
            {
                heading = GetNewHeading(heading, instruction.direction);
                for (var i = 0; i < instruction.distance; i++)
                {
                    position += heading;
                    if (part2 == 0)
                        if (visited.Contains(position))
                            part2 = GetManhatanDistance(position);
                        else
                            visited.Add(position);
                }
            }
            return (GetManhatanDistance(position), part2);
        }

        static Regex instructionRegex = new Regex(@"(?<direction>L|R)(?<distance>\d+)", RegexOptions.Compiled);
        static IEnumerable<Instruction> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : instructionRegex.Matches(File.ReadAllText(filePath)).Select(match => 
                new Instruction(match.Groups["direction"].Value[0], int.Parse(match.Groups["distance"].Value))
            );

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
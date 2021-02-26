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
    record Instruction(char direction, int value);

    class Program
    {
        static Dictionary<char, Complex> CARDINAL_DIRECTIONS = new Dictionary<char, Complex> {
            { 'N', Complex.ImaginaryOne },
            { 'S', -Complex.ImaginaryOne },
            { 'E', 1 },
            { 'W', -1 }
        };
        static Dictionary<char, Complex> ROTATIONS = new Dictionary<char, Complex> {
            { 'L', Complex.ImaginaryOne },
            { 'R', -Complex.ImaginaryOne }
        };
        static int Navigate(IEnumerable<Instruction> instructions, Complex heading, bool headingOnCardinal)
        {
            Complex position = 0;
            foreach (var (direction, value) in instructions)
                if (CARDINAL_DIRECTIONS.ContainsKey(direction))
                     if (headingOnCardinal)
                        heading += CARDINAL_DIRECTIONS[direction] * value;
                    else
                        position += CARDINAL_DIRECTIONS[direction] * value;
                else if (ROTATIONS.ContainsKey(direction))
                    heading *= Complex.Pow(ROTATIONS[direction], value / 90);
                else if (direction == 'F')
                    position += heading * value;
            return (int)(Math.Ceiling(Math.Abs(position.Real)) + Math.Ceiling(Math.Abs(position.Imaginary)));
        }

        static (int, int) Solve(IEnumerable<Instruction> instructions)
            => (
                Navigate(instructions, 1, false),
                Navigate(instructions, new Complex(10, 1), true)
            );

        static Regex lineRegex = new Regex(@"^(?<direction>[NSEWLRF])(?<value>\d+)$", RegexOptions.Compiled);
        static IEnumerable<Instruction> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath).Select(line => {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return new Instruction(match.Groups["direction"].Value[0], int.Parse(match.Groups["value"].Value));
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
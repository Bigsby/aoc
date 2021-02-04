using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        record Instruction(string Action, int Xstart, int Ystart, int Xend, int Yend) { }    

        const int MATRIX_SIDE = 1000;
        static int RunMatrix(IEnumerable<Instruction> instructions, Dictionary<string, Func<int,int>> updateFuncs)
        {
            var matrix = new Dictionary<int, int>();
            foreach (var index in Enumerable.Range(0, MATRIX_SIDE * MATRIX_SIDE))
                    matrix[(index / MATRIX_SIDE) % MATRIX_SIDE + (index % MATRIX_SIDE) * MATRIX_SIDE] = 0;
            foreach (var intruction in instructions)
                foreach (var x in Enumerable.Range(intruction.Xstart, intruction.Xend - intruction.Xstart + 1))
                    foreach (var y in Enumerable.Range(intruction.Ystart, intruction.Yend - intruction.Ystart + 1))
                    {
                        var position = x + y * MATRIX_SIDE;
                        matrix[position] = updateFuncs[intruction.Action](matrix[position]);
                    }
            return matrix.Values.Sum();
        }

        static int Part1(IEnumerable<Instruction> instructions)
            => RunMatrix(instructions, new Dictionary<string, Func<int, int>> {
                { "turn on", _ => 1 },
                { "toggle", value => value == 1 ? 0 : 1 },
                { "turn off", _ => 0 }
            });

        static int Part2(IEnumerable<Instruction> instructions)
            => RunMatrix(instructions, new Dictionary<string, Func<int, int>> {
                { "turn on", value => value + 1 },
                { "toggle", value => value + 2 },
                { "turn off", value => value > 0 ? value - 1 : 0 }
            });

        static Regex lineRegex = new Regex(@"^(toggle|turn off|turn on)\s(\d{1,3}),(\d{1,3})\sthrough\s(\d{1,3}),(\d{1,3})$", RegexOptions.Compiled);
        static IEnumerable<Instruction> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(line => {
                Match match = lineRegex.Match(line);
                if (match.Success)
                    return new Instruction(
                        match.Groups[1].Value,
                        int.Parse(match.Groups[2].Value),
                        int.Parse(match.Groups[3].Value),
                        int.Parse(match.Groups[4].Value),
                        int.Parse(match.Groups[5].Value));
                throw new Exception($"Bad format '{line}'");
            });
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
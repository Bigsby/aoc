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
        record Instruction(int Action, int Xstart, int Ystart, int Xend, int Yend) { }

        const int TURN_ON = 0;
        const int TOGGLE = 1;
        const int TURN_OFF = 2;
        static Dictionary<string, int> ACTIONS = new Dictionary<string, int> {
            { "turn on", TURN_ON },
            { "toggle", TOGGLE },
            { "turn off", TURN_OFF },
        };
        const int MATRIX_SIDE = 1000;
        static int RunMatrix(IEnumerable<Instruction> instructions, Func<int, int, int> updateFunc)
        {
            var matrix = new int[MATRIX_SIDE * MATRIX_SIDE];
            foreach (var intruction in instructions)
                foreach (var x in Enumerable.Range(intruction.Xstart, intruction.Xend - intruction.Xstart + 1))
                    foreach (var y in Enumerable.Range(intruction.Ystart, intruction.Yend - intruction.Ystart + 1))
                    {
                        var position = x + y * MATRIX_SIDE;
                        matrix[position] = updateFunc(intruction.Action, matrix[position]);
                    }
            return matrix.Sum();
        }

        static (int, int) Solve(IEnumerable<Instruction> instructions)
            => (
                RunMatrix(instructions, (action, value) => action switch
                {
                    TURN_ON => 1,
                    TOGGLE => value == 1 ? 0 : 1,
                    TURN_OFF => 0,
                    _ => throw new Exception($"Uknow action '{action}'")
                }),
                RunMatrix(instructions, (action, value) => action switch
                {
                    TURN_ON => value + 1,
                    TOGGLE => value + 2,
                    TURN_OFF => value > 0 ? value - 1 : 0,
                    _ => throw new Exception($"Uknow action '{action}'")
                })
            );

        static Regex lineRegex = new Regex(@"^(toggle|turn off|turn on)\s(\d{1,3}),(\d{1,3})\sthrough\s(\d{1,3}),(\d{1,3})$", RegexOptions.Compiled);
        static IEnumerable<Instruction> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line =>
            {
                Match match = lineRegex.Match(line);
                if (match.Success)
                    return new Instruction(
                        ACTIONS[match.Groups[1].Value],
                        int.Parse(match.Groups[2].Value),
                        int.Parse(match.Groups[3].Value),
                        int.Parse(match.Groups[4].Value),
                        int.Parse(match.Groups[5].Value));
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
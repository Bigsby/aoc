using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    record Command(Complex direction, int units);

    static class Program
    {
        static int Part1(IEnumerable<Command> commands)
        { 
            var position = Complex.Zero;
            foreach (var command in commands)
                position += command.direction * command.units;
            return (int)(position.Real * position.Imaginary);
        }

        static int Part2(IEnumerable<Command> commands)
        {
            var position = Complex.Zero;
            var aim = Complex.Zero;
            foreach (var command in commands)
                if (command.direction == 1)
                    position += command.units * (1 + aim);
                else
                    aim += command.direction * command.units;
            return (int)(position.Real * position.Imaginary);
        }

        static (int, int) Solve(IEnumerable<Command> puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static IEnumerable<Command> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => {
                var split = line.Split(' ');
                var units = int.Parse(split[1]);
                switch (split[0])
                {
                    case "forward": return new Command(new Complex(1, 0), units);
                    case "down": return new Command(new Complex(0, 1), units);
                    case "up": return new Command(new Complex(0, -1), units);
                    default: throw new Exception($"Unknow direction {split[0]}");
                };
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

using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;

namespace AoC
{
    static class Program
    {
        static (int, object) Solve(string[][] instructions)
        {
            var target = int.Parse(instructions[1][1]) * int.Parse(instructions[2][1]);
            var a = 1;
            while (a < target)
                if (a % 2 == 0)
                    a = a * 2 + 1;
                else
                    a *= 2;
            return (a - target, null);
        }

        static string[][] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath).Select(line => line.Split(' ')).ToArray();

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

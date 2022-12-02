using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<Tuple<int, int>>;
    static class Program
    {
        static int HandResult(int elf, int me)
            => elf == me ? 1 : 2 * ((elf + 1) % 3 == me ? 1 : 0);
        
        static int Part1(Input puzzleInput)
            => puzzleInput.Sum(hand => 3 * HandResult(hand.Item1, hand.Item2) + hand.Item2 + 1);

        static int Part2(Input puzzleInput)
            => puzzleInput.Sum(hand => 1 + (hand.Item2 * 3) + ((hand.Item1 + hand.Item2 + 2) % 3));

        static (int, int) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => Tuple.Create(line[0] - 'A', line[2] - 'X'));

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

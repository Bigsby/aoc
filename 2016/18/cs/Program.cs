using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Tiles = IEnumerable<bool>;

    static class Program
    {
        static void PrintTiles(IEnumerable<bool> list) => WriteLine(string.Join("", list.Select(v => v ? '.' : '^')));

        static (int, int) Solve(Tiles tiles)
        {
            var tileCount = tiles.Count();
            var safe = tiles.Count(t => t);
            var part1Result = 0;
            foreach (var step in Enumerable.Range(1, 400_000 - 1))
            {
                if (step == 40)
                    part1Result = safe;
                tiles = Enumerable.Range(0, tileCount)
                    .Select(index => (index == 0 || tiles.ElementAt(index - 1)) == (index == tileCount - 1 || tiles.ElementAt(index + 1)))
                    .ToArray();
                safe += tiles.Count(t => t);
            }
            return (part1Result, safe);
        }

        static Tiles GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim().Select(c => c == '.');

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

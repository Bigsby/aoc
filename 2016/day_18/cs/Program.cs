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
        static void PrintTiles(IEnumerable<bool> list) => WriteLine(string.Join("", list.Select(v => v ? '.' : '^' )));

        static int GetSafeCount(Tiles tiles, int count)
        {
            var tileCount = tiles.Count();
            var safe = tiles.Count(t => t);
            foreach (var _ in Enumerable.Range(0, count - 1))
            {
                tiles = Enumerable.Range(0, tileCount)
                    .Select(index => (index == 0 || tiles.ElementAt(index - 1)) == (index == tileCount - 1 || tiles.ElementAt(index + 1)))
                    .ToArray();
                safe += tiles.Count(t => t);
            }
            return safe;
        }

        static int Part1(Tiles tiles) => GetSafeCount(tiles, 40);

        static int Part2(Tiles tiles) => GetSafeCount(tiles, 400_000);

        static Tiles GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim().Select(c => c == '.');
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

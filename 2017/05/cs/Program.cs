using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    class Program
    {
        static int DoJumps(IEnumerable<int> jumps, Func<int, int> newJumpFunc)
        {
            var jumpList = jumps.ToList();
            var maxIndex = jumpList.Count;
            var currentIndex = 0;
            var count = 0;
            while (currentIndex >= 0 && currentIndex < maxIndex)
            {
                count++;
                var offset = jumpList[currentIndex];
                var nextIndex = currentIndex + offset;
                jumpList[currentIndex] = offset + newJumpFunc(offset);
                currentIndex = nextIndex;
            }
            return count;
        }

        static (int, int) Solve(IEnumerable<int> jumps)
            => (
                DoJumps(jumps, offset => 1),
                DoJumps(jumps, offset => offset < 3 ? 1 : -1)
            );

        static IEnumerable<int> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => int.Parse(line));

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
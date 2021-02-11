using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Scanners = Dictionary<int,int>;

    class Program
    {
        static Scanners GetCycles(Scanners scanners)
            => scanners.ToDictionary(kv => kv.Key, kv => 2 * (kv.Value - 1));

        static int Part1(Scanners scanners)
        {
            var cycles = GetCycles(scanners);
            var severity = 0;
            foreach (var currentLayer in Enumerable.Range(0, scanners.Keys.Max() + 1))
                if (cycles.ContainsKey(currentLayer) && currentLayer % cycles[currentLayer] == 0)
                    severity += currentLayer * scanners[currentLayer];
            return severity;
        }

        static bool RunPacketUntilCaugth(Scanners cycles, int offset)
        {
            foreach (var currentLayer in Enumerable.Range(0, cycles.Keys.Max() + 1))
                if (cycles.ContainsKey(currentLayer) && (currentLayer + offset) % cycles[currentLayer] == 0)
                    return false;
            return true;
        }

        static int Part2(Scanners scanners)
        {
            var cycles = GetCycles(scanners);
            var offset = 1;
            while (!RunPacketUntilCaugth(cycles, offset))
                offset++;
            return offset;
        }

        static Scanners GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line => {
                var split = line.Trim().Split(":");
                return (int.Parse(split[0].Trim()), int.Parse(split[1].Trim()));
            }).ToDictionary(split => split.Item1, split => split.Item2);
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
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
        static int Part1(Scanners scanners, Scanners cycles)
        {
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

        static int Part2(Scanners cycles)
        {
            var offset = 1;
            while (!RunPacketUntilCaugth(cycles, offset))
                offset++;
            return offset;
        }

        static (int, int) Solve(Scanners scanners)
        {
            var cycles = scanners.ToDictionary(kv => kv.Key, kv => 2 * (kv.Value - 1));
            return (
                Part1(scanners, cycles),
                Part2(cycles)
            );
        }

        static Scanners GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath).Select(line => {
                var split = line.Trim().Split(":");
                return (int.Parse(split[0].Trim()), int.Parse(split[1].Trim()));
            }).ToDictionary(split => split.Item1, split => split.Item2);

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
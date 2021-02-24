using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;

namespace AoC
{
    static class Program
    {
        static string GetChecksum(string data, int diskLength)
        {
            while (data.Length < diskLength)
                data += "0" + new string(data.Reverse().Select(c => c == '0' ? '1' : '0').ToArray());
            data = data[Range.EndAt(diskLength)];
            while (data.Length % 2 == 0)
                data = new string(Enumerable.Range(0, data.Length / 2)
                    .Select(index => data[2 * index] == data[2 * index + 1] ? '1' : '0' ).ToArray());
            return data;
        }

        static string Part1(string data) => GetChecksum(data, 272);

        static string Part2(string data) => GetChecksum(data, 35651584);

        static string GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim();
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
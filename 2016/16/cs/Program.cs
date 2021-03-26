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
                    .Select(index => data[2 * index] == data[2 * index + 1] ? '1' : '0').ToArray());
            return data;
        }

        static (string, string) Solve(string data)
            => (
                GetChecksum(data, 272),
                GetChecksum(data, 35651584)
            );

        static string GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim();

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
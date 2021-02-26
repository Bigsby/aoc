using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    static class Program
    {
        static int[] PATTERN = new [] { 0, 1, 0, -1 };
        static int GetValue(int offset, IEnumerable<int> signal)
        {
            var total = 0;
            foreach (var (number, index) in signal.Select((number, index) => (number, index)))
            {
                var indexInPattern = ((index + 1) / offset) % PATTERN.Length;
                var multiplier = PATTERN[indexInPattern];
                total += number * multiplier;
            }
            return Math.Abs(total) % 10;
        }

        static IEnumerable<int> NextPhase(IEnumerable<int> signal)
        {
            var result = new List<int>();
            foreach (var (number, index) in signal.Select((number, index) => (number, index)))
                result.Add(GetValue(index + 1, signal));
            return result;
        }

        static string Part1(IEnumerable<int> signal)
        {
            signal = signal.ToList();
            foreach (var _ in Enumerable.Range(0, 100))
                signal = NextPhase(signal);
            return string.Join("", signal.Take(8));
        }

        static string Part2(IEnumerable<int> signal)
        {
            var offset = int.Parse(string.Join("", signal.Take(7)));
            var signalArray = Enumerable.Repeat(signal, 10_000).SelectMany(inSignal => inSignal).Skip(offset).ToArray();
            foreach (var _ in Enumerable.Range(0, 100))
            {
                var sum = 0;
                for (var index = signalArray.Length - 1; index >= 0; index--)
                    signalArray[index] = sum = (sum + signalArray[index]) % 10;
            }
            return string.Join("", signalArray.Take(8));
        }

        static (string, string) Solve(IEnumerable<int> signal)
            => (
                Part1(signal),
                Part2(signal)
            );

        static IEnumerable<int> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim().Select(c => int.Parse(c.ToString()));

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

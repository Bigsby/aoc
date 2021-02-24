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
                for (var i = signalArray.Length - 1; i >= 0; i--)
                    signalArray[i] = sum = (sum + signalArray[i]) % 10;
            }
            return string.Join("", signalArray.Take(8));
        }

        static IEnumerable<int> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim().Select(c => int.Parse(c.ToString()));
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

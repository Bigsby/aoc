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
        static Dictionary<int, Dictionary<char, int>> GetColumnRecords(IEnumerable<string> messages)
        {
            var columnRecords = new Dictionary<int, Dictionary<char, int>>();
            foreach (var index in Enumerable.Range(0, messages.First().Length))
                columnRecords[index] = new Dictionary<char, int>();
            foreach (var message in messages)
                foreach (var (c, column) in message.Select((c, column) => (c, column)))
                    if (columnRecords[column].ContainsKey(c))
                        columnRecords[column][c]++;
                    else
                        columnRecords[column][c] = 1;
            return columnRecords;
        }

        static string Part1(IEnumerable<string> messages)
        {
            var columnRecords = GetColumnRecords(messages);
            return Enumerable.Range(0, messages.First().Length).Aggregate("", (soFar, column) =>
                soFar + columnRecords[column].Aggregate((max, current) => max.Value > current.Value ? max : current).Key
            );
        }

        static string Part2(IEnumerable<string> messages)
        {
            var columnRecords = GetColumnRecords(messages);
            return Enumerable.Range(0, messages.First().Length).Aggregate("", (soFar, column) =>
                soFar + columnRecords[column].Aggregate((min, current) => min.Value < current.Value ? min : current).Key
            );
        }

        static IEnumerable<string> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath);
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
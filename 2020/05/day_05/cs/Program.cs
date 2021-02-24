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
        static int Part1(IEnumerable<int> seats) => seats.Max();

        static int Part2(IEnumerable<int> seats)
        {
            var lastId = seats.Min();
            foreach (var currentId in seats.OrderBy(id => id))
            {
                if (currentId - lastId == 2)
                    return lastId + 1;
                lastId = currentId;
            }
            throw new Exception("Seat not found");
        }

        static Dictionary<char, char> REPLACEMENTS = new Dictionary<char, char> { 
            { 'B', '1' },
            { 'F', '0' },
            { 'R', '1' },
            { 'L', '0' }
        };
        static IEnumerable<int> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(line => 
                Convert.ToInt32(REPLACEMENTS.Aggregate(line, (soFar, pair) => soFar.Replace(pair.Key, pair.Value)), 2));
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
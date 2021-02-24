using System;
using static System.Console;
using System.IO;
using System.Diagnostics;

namespace AoC
{
    class Program
    {
        const char GROUP_START = '{';
        const char GROUP_END = '}';
        const char GARBAGE_START = '<';
        const char GARBAGE_END = '>';
        const char ESCAPE = '!';
        static (int groupScore, int garbageCount) Count(string stream)
        {
            var groupScore = 0;
            var garbageCount = 0;
            var depth = 0;
            var inGarbage = false;
            var escape = false;
            foreach (var c in stream)
                if (escape)
                    escape = false;
                else if (inGarbage)
                    if (c == ESCAPE)
                        escape = true;
                    else if (c == GARBAGE_END)
                        inGarbage = false;
                    else
                        garbageCount++;
                else if (c == GARBAGE_START)
                    inGarbage = true;
                else if (c == GROUP_START)
                    depth++;
                else if (c == GROUP_END)
                {
                    groupScore += depth;
                    depth--;
                }
            return (groupScore, garbageCount);
        }

        static int Part1(string stream) => Count(stream).groupScore;

        static int Part2(string stream) => Count(stream).garbageCount;

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
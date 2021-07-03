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
        static (int groupScore, int garbageCount) Solve(string stream)
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
                    groupScore += depth--;
            return (groupScore, garbageCount);
        }

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

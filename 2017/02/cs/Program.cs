using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        static (int, int) Solve(int[][] lines)
        {
            var total1 = 0;
            var total2 = 0;
            foreach (var line in lines)
            {
                total1 += line.Max() - line.Min();
                foreach (var numberA in line)
                    foreach(var numberB in line)
                        if (numberA > numberB && numberA % numberB == 0)
                            total2 += numberA / numberB;
            }
            return (total1, total2);
        }

        static Regex lineRegex = new Regex(@"\d+", RegexOptions.Compiled);
        static int[][] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath)
                .Select(line => 
                lineRegex.Matches(line).Select(match => int.Parse(match.Groups[0].Value)).ToArray()).ToArray();

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
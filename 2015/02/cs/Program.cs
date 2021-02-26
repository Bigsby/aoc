using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Text.RegularExpressions;
using System.Collections.Generic;

namespace AoC
{
    class Program
    {
        static int Part1(IEnumerable<Tuple<int, int, int>> dimensions)
        {
            var totalPaper = 0;
            foreach (var dimension in dimensions)
            {
                var (w, l, h) = dimension;
                var wl = w * l;
                var wh = w * h;
                var hl = h * l;
                var smallest = Enumerable.Min(new int[] { wl, wh, hl });
                totalPaper += 2 * (wl + wh + hl) + smallest;
            }
            return totalPaper;
        }

        static int Part2(IEnumerable<Tuple<int, int, int>> dimensions)
        {
            var totalRibbon = 0;
            foreach (var dimension in dimensions)
            {
                var (w, l, h) = dimension;
                var sideList = new int[] { w, l, h }.ToList();
                sideList.Remove(Enumerable.Max(sideList));
                totalRibbon += 2 * (sideList[0] + sideList[1]) + w * l * h;
            }
            return totalRibbon;
        }

        static (int, int) Solve(IEnumerable<Tuple<int, int, int>> dimensions)
            => (Part1(dimensions), Part2(dimensions));


        static Regex lineRegex = new Regex(@"^(\d+)x(\d+)x(\d+)$", RegexOptions.Compiled);
        static IEnumerable<Tuple<int, int, int>> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            foreach (var line in File.ReadAllLines(filePath))
            {
                var match = lineRegex.Match(line);
                if (match.Success)
                {
                    yield return new Tuple<int, int, int>(
                        int.Parse(match.Groups[1].Value),
                        int.Parse(match.Groups[2].Value),
                        int.Parse(match.Groups[3].Value)
                    );
                }
            }
        }

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
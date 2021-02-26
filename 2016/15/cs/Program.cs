using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    record Disc
    {
        public int Positions { get; }
        public int Offset { get; }
        public Disc(int positions, int start, int index)
        {
            Positions = positions;
            Offset = start + index + 1;
        }
    }
    
    class Program
    {
        static int FindWinningPosiiton(IEnumerable<Disc> discs)
        {
            var jump = 1;
            var offset = 0;
            foreach (var disc in discs)
            {
                while ((offset + disc.Offset) % disc.Positions != 0)
                    offset += jump;
                jump *= disc.Positions;
            }
            return offset;
        }

        static (int, int) Solve(IEnumerable<Disc> discs)
            => (
                FindWinningPosiiton(discs),
                FindWinningPosiiton(discs.Concat(new[] { new Disc(11, 0, discs.Count()) }))
            );

        static Regex lineRegex = new Regex(@"^Disc #\d has (?<positions>\d+) positions; at time=0, it is at position (?<start>\d+).$", RegexOptions.Compiled);
        static IEnumerable<Disc> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath).Select((line, index) =>
            {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return new Disc(
                        int.Parse(match.Groups["positions"].Value),
                        int.Parse(match.Groups["start"].Value),
                        index
                    );
                throw new Exception($"Bad format '{line}'");
            });

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
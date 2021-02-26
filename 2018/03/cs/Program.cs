using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Claim = Tuple<int,int,int,int,int>;

    class Program
    {
        static Dictionary<Tuple<int, int>, int> GetCoveredPoints(Claim[] claims)
        {
            var coveredPoints = new Dictionary<Tuple<int, int>, int>();
            foreach (var (_, left, top, width, height) in claims)
                foreach (var x in Enumerable.Range(left, width))
                    foreach (var y in Enumerable.Range(top, height))
                    {
                        var point = Tuple.Create(x, y);
                        if (coveredPoints.ContainsKey(point))
                            coveredPoints[point]++;
                        else
                            coveredPoints[point] = 1;
                    }
            return coveredPoints;
        }
        
        static int Part2(Claim[] claims, Dictionary<Tuple<int, int>, int> coveredPoints)
        {
            foreach (var (id, left, top, width, height) in claims)
            {
                var allOne = true;
                foreach (var x in Enumerable.Range(left, width))
                    foreach (var y in Enumerable.Range(top, height))
                        allOne &= coveredPoints[Tuple.Create(x, y)] == 1;
                if (allOne)
                    return id;
            }
            throw new Exception("Claim not found");
        }

        static (int, int) Solve(Claim[] claims)
        {
            var coveredPoints = GetCoveredPoints(claims);
            return (
                coveredPoints.Values.Count(value => value > 1),
                Part2(claims, coveredPoints)
            );
        }

        static Regex lineRegex = new Regex(@"^#(?<id>\d+)\s@\s(?<left>\d+),(?<top>\d+):\s(?<width>\d+)x(?<height>\d+)$");
        static Claim[] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => {
                Match match = lineRegex.Match(line);
                return Tuple.Create(
                    int.Parse(match.Groups["id"].Value), 
                    int.Parse(match.Groups["left"].Value), 
                    int.Parse(match.Groups["top"].Value), 
                    int.Parse(match.Groups["width"].Value), 
                    int.Parse(match.Groups["height"].Value)
                );
            }).ToArray();

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
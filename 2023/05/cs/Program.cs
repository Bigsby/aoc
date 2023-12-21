using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Diagnostics.Contracts;
using System.Runtime.InteropServices;

namespace AoC
{
    using Input = Tuple<List<int>,Dictionary<string,string>,Dictionary<Tuple<string,string>,List<Tuple<int,int,int>>>>;

    static class Program
    {
        static int Part1(Input puzzleInput)
        { 
            var lowestLocation = int.MaxValue;
            var (seeds, paths, maps) = puzzleInput;
            foreach (var seed in seeds)
            {
                var current = seed;
                var source = "seed";
                while (paths.ContainsKey(source))
                {
                    var destination = paths[source];
                    foreach (var (destinationStart, sourceStart, length) in maps[Tuple.Create(source, destination)])
                        if (current >= sourceStart && current < sourceStart + length)
                        {
                            current += destinationStart - sourceStart;
                            break;
                        }
                    source = destination;
                }
                lowestLocation = lowestLocation < current ? lowestLocation : current;
            }
            return lowestLocation;
        }

        static int Part2(Input puzzleInput)
        {
            return 2;
        }

        static (int, int) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath))
                throw new FileNotFoundException(filePath);
            var seeds = new List<int>();
            var paths = new Dictionary<string, string>();
            var maps = new Dictionary<Tuple<string,string>,List<Tuple<int,int,int>>>(); 
            var destination = "";
            var source = "";
            foreach (var line in File.ReadAllLines(filePath))
            {
                var strippedLine = line.Trim();
                if (strippedLine.StartsWith("seeds:")) {
                    seeds = strippedLine.Split(':')[1].Split(' ', StringSplitOptions.RemoveEmptyEntries).Select(int.Parse).ToList();
                    continue;
                }
                if (string.IsNullOrEmpty(strippedLine))
                    continue;
                if (!char.IsDigit(strippedLine[0]))
                {
                    var splits = strippedLine.Split('-');
                    source = splits[0];
                    destination = splits[2].Split(' ')[0];
                    paths[source] = destination;
                }
                else
                {
                    var splits = strippedLine.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                    var key =Tuple.Create(source, destination);
                    if (!maps.ContainsKey(key))
                        maps[key] = new List<Tuple<int, int, int>>();
                    maps[key].Add(Tuple.Create(int.Parse(splits[0]), int.Parse(splits[1]), int.Parse(splits[2])));
                }
            }
            return Tuple.Create(seeds, paths, maps);
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

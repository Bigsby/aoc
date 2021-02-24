using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    record Entry(string name, int speed, int duration, int rest);

    static class Program
    {
        const int TIME = 2503;

        static int CalculateDistance(Entry entry, int totalDuration)
        {
            var period = entry.duration + entry.rest;
            var periods = Math.DivRem(totalDuration, period, out var remainder);
            var total = periods * entry.speed * entry.duration;
            return total + entry.speed * Math.Min(remainder, entry.duration);
        }

        static int Part1(IEnumerable<Entry> entries) => entries.Max(entry => CalculateDistance(entry, TIME));

        static int GetDistanceForTime(Entry entry, int time) 
            => time % (entry.duration + entry.rest) < entry.duration ? entry.speed : 0;

        class Deer 
        {
            public Entry Entry { get; init; }
            public int Distance { get; set; }
            public int Points { get; set; }
            public Deer(Entry entry) => Entry = entry;
        }

        static int Part2(IEnumerable<Entry> entries)
        {
            var deers = entries.Select(entry => new Deer(entry)).ToArray();
            for (var time = 0; time < TIME; time++)
            {
                var maxDistance = 0;
                foreach (var deer in deers)
                {
                    deer.Distance += GetDistanceForTime(deer.Entry, time);
                    maxDistance = Math.Max(maxDistance, deer.Distance);
                }
                foreach (var deer in deers)
                    if (deer.Distance == maxDistance)
                        deer.Points++;
            }
            return deers.Max(deer => deer.Points);
        }

        static Regex lineRegex = new Regex(@"^(\w+)\scan\sfly\s(\d+)\skm/s\sfor\s(\d+)\sseconds,\sbut\sthen\smust\srest\sfor\s(\d+)\sseconds.$", RegexOptions.Compiled);
        static IEnumerable<Entry> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line => {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return new Entry(
                        match.Groups[1].Value,
                        int.Parse(match.Groups[2].Value),
                        int.Parse(match.Groups[3].Value),
                        int.Parse(match.Groups[4].Value)
                    );
                throw new Exception($"Bad format '${line}'");
            });
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
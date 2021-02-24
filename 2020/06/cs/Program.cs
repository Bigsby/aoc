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
        record Group(int PeopleCount, Dictionary<char, int> Record);

        static int Part1(IEnumerable<Group> groups) => groups.Sum(group => group.Record.Keys.Count());

        static int Part2(IEnumerable<Group> groups) => groups.Sum(group => 
            group.Record.Keys.Count(letter => group.Record[letter] == group.PeopleCount));

        static IEnumerable<Group> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Split("\n\n").Select(entry => {
                var record = new Dictionary<char, int>();
                var peopleCount = 0;
                foreach (var line in entry.Split('\n'))
                {
                    if (!string.IsNullOrEmpty(line))
                        peopleCount++;
                    foreach (var c in line)
                        if (record.ContainsKey(c))
                            record[c]++;
                        else
                            record[c] = 1;
                }
                return new Group(peopleCount, record);
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
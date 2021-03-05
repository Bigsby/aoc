using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    record Group(int PeopleCount, IEnumerable<int> Record);

    class Program
    {
        static (int, int) Solve(IEnumerable<Group> groups)
            => (
                groups.Sum(group => group.Record.Count()),
                groups.Sum(group =>
                    group.Record.Count(count => count == group.PeopleCount))
            );

        static IEnumerable<Group> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Split("\n\n").Select(entry =>
            {
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
                return new Group(peopleCount, record.Values);
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
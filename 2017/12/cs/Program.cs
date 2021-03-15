using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Connections = Dictionary<int, List<int>>;

    class Program
    {
        static HashSet<int> GetProgramGroup(int program, Connections connections)
        {
            var result = new HashSet<int>();
            result.Add(program);
            var queue = new Queue<int>();
            queue.Enqueue(program);
            while (queue.Any())
                foreach (var connection in connections[queue.Dequeue()])
                    if (!result.Contains(connection))
                    {
                        result.Add(connection);
                        queue.Enqueue(connection);
                    }
            return result;
        }

        static (int, int) Solve(Connections connections)
        {
            var part1Result = GetProgramGroup(0, connections).Count;
            var groupsCount = 0;
            while (connections.Count > 0)
            {
                groupsCount++;
                foreach (var connection in GetProgramGroup(connections.Keys.First(), connections))
                    if (connections.ContainsKey(connection))
                        connections.Remove(connection);
            }
            return (part1Result, groupsCount);
        }

        static Regex lineRegex = new Regex(@"^(?<one>\d+)\s<->\s(?<two>.*)$", RegexOptions.Compiled);
        static Connections GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath).Select(line =>
            {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return (int.Parse(match.Groups["one"].Value), match.Groups["two"].Value.Split(",").Select(int.Parse).ToList());
                throw new Exception($"Bad format '{line}'");
            }).ToDictionary(record => record.Item1, record => record.Item2);

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
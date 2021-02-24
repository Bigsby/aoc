using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Connections = Dictionary<int,List<int>>;

    class Program
    {
        static HashSet<int> GetProgramGroup(int program, Connections connections, HashSet<int> soFar)
        {
            soFar.Add(program);
            foreach (var connection in connections[program])
                if (!soFar.Contains(connection))
                    soFar.UnionWith(GetProgramGroup(connection, connections, soFar));
            return soFar;
        }

        static int Part1(Connections connections) => GetProgramGroup(0, connections, new HashSet<int>()).Count;

        static int Part2(Connections connections)
        {
            var groupsCount = 0;
            while (connections.Count > 0)
            {
                groupsCount++;
                foreach (var connection in GetProgramGroup(connections.Keys.First(), connections, new HashSet<int>()))
                    if (connections.ContainsKey(connection))
                        connections.Remove(connection);
            }
            return groupsCount;
        }

        static Regex lineRegex = new Regex(@"^(?<one>\d+)\s<->\s(?<two>.*)$", RegexOptions.Compiled);
        static Connections GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line => {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return (int.Parse(match.Groups["one"].Value), match.Groups["two"].Value.Split(",").Select(int.Parse).ToList());
                throw new Exception($"Bad format '{line}'");
            }).ToDictionary(record => record.Item1, record => record.Item2);
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
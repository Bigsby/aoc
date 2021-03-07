using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    record Pair(char Dependency, char Dependant);
    
    class Program
    {
        static Dictionary<char, List<char>> BuildDependencyGraph(IEnumerable<Pair> pairs)
        {
            var dependencies = new Dictionary<char, List<char>>();
            foreach (var pair in pairs)
            {
                if (!dependencies.ContainsKey(pair.Dependant))
                    dependencies[pair.Dependant] = new List<char>();
                if (!dependencies.ContainsKey(pair.Dependency))
                    dependencies[pair.Dependency] = new List<char>();
                dependencies[pair.Dependant].Add(pair.Dependency);
            }
            return dependencies;
        }

        static string Part1(Dictionary<char, List<char>> dependencies)
        {
            var path = new List<char>();
            while (dependencies.Count > 0)
            {
                var nextStep = dependencies.Where(pair => !pair.Value.Any()).Select(pair => pair.Key).OrderBy(step => step).First();
                dependencies.Remove(nextStep);
                path.Add(nextStep);
                foreach (var stepDependencies in dependencies.Values)
                    if (stepDependencies.Contains(nextStep))
                        stepDependencies.Remove(nextStep);
            }
            return new string(path.ToArray());
        }

        const int WORKER_COUNT = 5;
        const int STEP_DURATION_OFFSET = (int)'A' - 60 - 1;
        static int Part2(Dictionary<char, List<char>> dependencies)
        {
            var runningWorkers = new Dictionary<char, int>();
            var seconds = 0;
            while (dependencies.Any() || runningWorkers.Any())
            {
                var toRemove = new List<char>();
                foreach (var step in runningWorkers.Keys)
                {
                    runningWorkers[step]--;
                    if (runningWorkers[step] == 0)
                        toRemove.Add(step);
                }
                foreach (var step in toRemove)
                {
                    runningWorkers.Remove(step);
                    foreach (var stepDependencies in dependencies.Values)
                        if (stepDependencies.Contains(step))
                            stepDependencies.Remove(step);
                }
                foreach (var nextStep in dependencies.Where(pair => !pair.Value.Any()).Select(pair => pair.Key).OrderBy(step => step))
                {
                    if (runningWorkers.Count > WORKER_COUNT)
                        break;
                    runningWorkers[nextStep] = (int)nextStep - STEP_DURATION_OFFSET;
                    dependencies.Remove(nextStep);
                }
                seconds++;
            }
            return seconds - 1;
        }

        static (string, int) Solve(IEnumerable<Pair> pairs)
        {
            var dependencies = BuildDependencyGraph(pairs);
            return (
                Part1(dependencies.ToDictionary(kv => kv.Key, kv => kv.Value.ToList())),
                Part2(dependencies)
            );
        }

        static Regex lineRegex = new Regex(@"\s([A-Z])\s", RegexOptions.Compiled);
        static IEnumerable<Pair> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => {
                var matches = lineRegex.Matches(line);
                if (matches.Count == 2)
                    return new Pair(matches[0].Groups[1].Value[0], matches[1].Groups[1].Value[0]);
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
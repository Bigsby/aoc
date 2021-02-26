using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Entries = Dictionary<string, Dictionary<string, int>>;

    class Program
    {
        static IEnumerable<IEnumerable<T>> Permutations<T>(IEnumerable<T> values) where T : IComparable
        {
            if (values.Count() == 1)
                return new[] { values };
            return values.SelectMany(v => 
                Permutations(values.Where(x => x.CompareTo(v) != 0)), (v, p) => p.Prepend(v));
        }

        static int CalculateHappiness(string[] arrangement, Entries entries)
        {
            var total = 0;
            var length = arrangement.Count();
            foreach (var (person, index) in arrangement.Select((person, index) => (person, index)))
            {
                total += entries[person][arrangement[index > 0 ? index - 1 : length - 1]];
                total += entries[person][arrangement[index < length - 1 ? index + 1 : 0]];
            }
            return total;
        }

        static int Part1(Entries entries)
            => Permutations(entries.Keys).Max(arrangement => CalculateHappiness(arrangement.ToArray(), entries));

        static int Part2(Entries entries)
        {
            var me = "me";
            entries[me] = new Dictionary<string, int>();
            foreach(var person in entries.Keys.ToArray())
            {
                if (person == me)
                    continue;
                entries[me][person] = 0;
                entries[person][me] = 0;
            }
            return Part1(entries);
        }

        static (int, int) Solve(Entries entries)
            => (Part1(entries), Part2(entries));

        static Regex lineRegex = new Regex(@"^(\w+)\swould\s(gain|lose)\s(\d+)\shappiness\sunits\sby\ssitting\snext\sto\s(\w+)\.$", RegexOptions.Compiled);
        static Entries GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var entries = new Entries();
            foreach (var line in File.ReadLines(filePath))
            {
                var match = lineRegex.Match(line);
                if (match.Success)
                {
                    var target = match.Groups[1].Value;
                    if (!entries.ContainsKey(target))
                        entries[target] = new Dictionary<string, int>();
                    entries[target][match.Groups[4].Value] = 
                        (match.Groups[2].Value == "gain" ? 1 : -1) * int.Parse(match.Groups[3].Value);
                }
                else
                    throw new Exception($"Bad format '{line}'");
            }
            return entries;
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
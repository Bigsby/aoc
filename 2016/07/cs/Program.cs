using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        static Regex abbaRegex = new Regex(@"([a-z])((?!\1)[a-z])\2\1", RegexOptions.Compiled);
        static bool SupportsTLS(IEnumerable<string> ip)
            => !ip.Where((part, index) => index % 2 == 1).Any(hypernet => abbaRegex.Matches(hypernet).Any())
                &&
                ip.Where((part, index) => index % 2 == 0).Any(supernet => abbaRegex.Matches(supernet).Any());

        static int Part1(IEnumerable<IEnumerable<string>> ips) => ips.Count(SupportsTLS);

        static IEnumerable<string> FindBABs(string supernet)
            => Enumerable.Range(0, supernet.Length - 2).Where(index => supernet[index] == supernet[index + 2])
                .Select(index => new string(new [] { supernet[index + 1], supernet[index], supernet[index + 1] }));

        static bool SupportsSSL(IEnumerable<string> ip)
        {
            var babs = new HashSet<string>();
            foreach(var supernet in ip.Where((part, index) => index % 2 == 0))
                foreach(var bab in FindBABs(supernet))
                    babs.Add(bab);
            foreach (var hypernet in ip.Where((part, index) => index % 2 == 1))
                if (babs.Any(bab => hypernet.Contains(bab)))
                    return true;
            return false;
        }

        static int Part2(IEnumerable<IEnumerable<string>> ips) => ips.Count(SupportsSSL);

        static Regex lineRegex = new Regex(@"(\[?[a-z]+\]?)", RegexOptions.Compiled);
        static IEnumerable<IEnumerable<string>> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(line => lineRegex.Matches(line).Select(match => match.Groups[1].Value));
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
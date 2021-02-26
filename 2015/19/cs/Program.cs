using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    record Replacement(string source, string target);

    static class Program
    {
        static IEnumerable<string> ProcessReplacement(string molecule, Replacement replacement)
            => Regex.Matches(molecule, replacement.source).Select(match =>
                molecule[Range.EndAt(match.Index)] + replacement.target + molecule[Range.StartAt(match.Index + match.Length)]);

        static int Part1((IEnumerable<Replacement>, string) puzzleInput)
        {
            var (replacements, molecule) = puzzleInput;
            var newMolecules = new List<string>();
            foreach (var replacement in replacements)
                newMolecules.AddRange(ProcessReplacement(molecule, replacement));
            return newMolecules.Distinct().Count();
        }

        static string Reverse(string source)
            => new string(source.Reverse().ToArray());

        static int Part2((IEnumerable<Replacement>, string) puzzleInput)
        {
            var (replacements, molecule) = puzzleInput;
            var targetMolecule = "e";
            molecule = Reverse(molecule);
            var replacemntDict = replacements.ToDictionary(rep => Reverse(rep.target), rep => Reverse(rep.source));
            var count = 0;
            while (molecule != targetMolecule)
                molecule = Regex.Replace(molecule, string.Join("|", replacemntDict.Keys), match =>
                {
                    count++;
                    return replacemntDict[match.Value];
                });
            return count;
        }

        static (int, int) Solve((IEnumerable<Replacement>, string) puzzleInput)
        => (
            Part1(puzzleInput),
            Part2(puzzleInput)
        );

        static Regex lineRegex = new Regex(@"^(\w+)\s=>\s(\w+)$", RegexOptions.Compiled);
        static (IEnumerable<Replacement>, string) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var replacements = new List<Replacement>();
            var molecule = string.Empty;
            foreach (var line in File.ReadLines(filePath))
            {
                var match = lineRegex.Match(line);
                if (match.Success)
                    replacements.Add(new Replacement(match.Groups[1].Value, match.Groups[2].Value));
                else
                    molecule += line;
            }
            return (replacements, molecule);
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

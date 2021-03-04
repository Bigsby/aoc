using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Passport = Dictionary<string, string>;

    class Program
    {
        static string[] MANDATORY_FIELDS = { "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid" };

        static bool ValidateInt(string value, int min, int max)
            => int.TryParse(value, out var parsed) && parsed >= min && parsed <= max;

        static Regex hgtRegex = new Regex(@"^(\d{2,3})(cm|in)$", RegexOptions.Compiled);
        static bool ValidateHgt(string value)
        {
            Match match = hgtRegex.Match(value);
            if (match.Success)
            {
                var height = int.Parse(match.Groups[1].Value);
                if (match.Groups[2].Value == "cm")
                    return height is >= 150 and <= 193;
                else
                    return height is >= 59 and <= 76;
            }
            return false;
        }

        static Regex hclRegex = new Regex(@"^#[0-9a-f]{6}$", RegexOptions.Compiled);
        static string[] ECLS = new[] { "amb", "blu", "brn", "gry", "grn", "hzl", "oth" };
        static Regex pidRegex = new Regex(@"^[\d]{9}$", RegexOptions.Compiled);
        static (int, int) Solve(IEnumerable<Passport> passports)
            => (
                passports.Count(passport =>
                    MANDATORY_FIELDS.All(field => passport.ContainsKey(field))),
                passports.Count(passport =>
                    MANDATORY_FIELDS.All(field =>
                        passport.ContainsKey(field) &&
                        field switch
                        {
                            "byr" => ValidateInt(passport[field], 1920, 2002),
                            "iyr" => ValidateInt(passport[field], 2010, 2020),
                            "eyr" => ValidateInt(passport[field], 2020, 2030),
                            "hgt" => ValidateHgt(passport[field]),
                            "hcl" => hclRegex.Match(passport[field]).Success,
                            "ecl" => ECLS.Contains(passport[field]),
                            "pid" => pidRegex.Match(passport[field]).Success,
                            _ => throw new Exception($"No validation for field '{field}'")
                        }
                    )
                )
            );

        static Regex entryRegex = new Regex(@"([a-z]{3})\:([^\s]+)", RegexOptions.Compiled);
        static IEnumerable<Passport> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Split(Environment.NewLine + Environment.NewLine).Select(entry =>
                entryRegex.Matches(entry).ToDictionary(match => match.Groups[1].Value, match => match.Groups[2].Value));

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
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
        static int CountValidPassports(IEnumerable<Passport> passports, Func<Passport, bool> validationFunc)
            => passports.Count(passport => validationFunc(passport));

        static string[] MANDATORY_FIELDS = { "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid" };

        static int Part1(IEnumerable<Passport> passports)
            => CountValidPassports(passports, passport =>
                MANDATORY_FIELDS.All(field => passport.ContainsKey(field)));

        static bool ValidateInt(string value, int min, int max)
        {
            try
            {
                var parsed = int.Parse(value);
                return parsed >= min && parsed <= max;
            }
            catch
            {
                return false;
            }
        }

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
        static string[] ECLS = new [] { "amb", "blu", "brn", "gry", "grn", "hzl", "oth" };
        static Regex pidRegex = new Regex(@"^[\d]{9}$", RegexOptions.Compiled);
        static Dictionary<string, Func<string, bool>> VALIDATIONS = new Dictionary<string, Func<string, bool>> {
            { "byr", value => ValidateInt(value, 1920, 2002) },
            { "iyr", value => ValidateInt(value, 2010, 2020) },
            { "eyr", value => ValidateInt(value, 2020, 2030) },
            { "hgt", ValidateHgt },
            { "hcl", value => hclRegex.Match(value).Success },
            { "ecl", value => ECLS.Contains(value) },
            { "pid", value => pidRegex.Match(value).Success }
        };
        static int Part2(IEnumerable<Passport> passports)
            => CountValidPassports(passports, passport =>
                MANDATORY_FIELDS.All(field => passport.ContainsKey(field) && VALIDATIONS[field](passport[field])));

        static Regex entryRegex = new Regex(@"([a-z]{3})\:([^\s]+)", RegexOptions.Compiled);
        static IEnumerable<Passport> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Split(Environment.NewLine + Environment.NewLine).Select(entry =>
                entryRegex.Matches(entry).ToDictionary(match => match.Groups[1].Value, match => match.Groups[2].Value));
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
using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Security.Cryptography;
using System.Text;

namespace AoC
{
    static class Program
    {
        static Regex tripleRegex = new Regex(@"(.)\1{2}", RegexOptions.Compiled);
        static Regex quintetRegex = new Regex(@"(.)\1{4}", RegexOptions.Compiled);
        static int FindKey(string salt, int stretch)
        {
            var index = 0;
            var keys = new List<int>();
            var threes = "0123456789abcdef".ToDictionary(c => c, c => new List<int>());
            using (var md5 = MD5.Create())
            {
                while (keys.Count < 64)
                {
                    var value = salt + index.ToString();
                    foreach (var _ in Enumerable.Range(0, stretch + 1))
                    {
                        var hash = md5.ComputeHash(UTF8Encoding.UTF8.GetBytes(value));
                        value = BitConverter.ToString(hash).Replace("-", "").ToLower();
                    }
                    var match = quintetRegex.Match(value);
                    if (match.Success)
                    {
                        var digit = match.Groups[0].Value[0];
                        foreach (var tripletIndex in threes[digit])
                            if (index - tripletIndex <= 1000)
                                keys.Add(tripletIndex);
                        threes[digit].Clear();
                    }
                    match = tripleRegex.Match(value);
                    if (match.Success)
                        threes[match.Groups[0].Value[0]].Add(index);
                    index++;
                }
            }
            return keys.OrderBy(key => key).ElementAt(63);
        }

        static (int, int) Solve(string salt)
            => (
                FindKey(salt, 0),
                FindKey(salt, 2016)
            );

        static string GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim();

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
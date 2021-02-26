using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;

namespace AoC
{
    class Program
    {
        const string PREFIX = "00-00-0";

        static (string, string) Solve(string doorId)
        {
            var index = 0;
            var password1 = "";
            var password2 = new char[8];
            var missingIndexes = new List<char> { '0', '1', '2', '3', '4', '5', '6', '7' };
            using (var md5 = MD5.Create())
                while (missingIndexes.Any())
                {
                    var hash = md5.ComputeHash(UTF8Encoding.UTF8.GetBytes(doorId + index));
                    var result = BitConverter.ToString(hash);
                    if (result.StartsWith(PREFIX))
                    {
                        if (password1.Length< 8)
                            password1 += result[7];
                        var digitIndex = result[7];
                        if (missingIndexes.Contains(digitIndex))
                        {
                            password2[int.Parse(digitIndex.ToString())] = result[9];
                            missingIndexes.Remove(digitIndex);
                        }
                    }
                    index++;
                }
            return (password1.ToLower(), string.Join("", password2).ToLower());
        }

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
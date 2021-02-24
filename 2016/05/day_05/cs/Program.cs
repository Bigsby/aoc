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
        const string PREFIX = "00000";
        static Encoding ENCODING = UTF8Encoding.UTF8;
        
        static string Part1(string doorId)
        {
            var index = 0;
            var password = "";
            using (var md5 = MD5.Create())
                while (password.Length < 8)
                {
                    var hash = md5.ComputeHash(ENCODING.GetBytes(doorId + index.ToString()));
                    var result = string.Join("", (hash).Select(hashByte => hashByte.ToString("x2")));
                    if (result.StartsWith(PREFIX))
                        password += result[5];
                    index++;
                }
            return password;
        }

        static string Part2(string doorId)
        {
            var index = 0;
            var password = new char[8];
            var missingIndexes = new List<char> { '0', '1', '2', '3', '4', '5', '6', '7' };
            using (var md5 = MD5.Create())
                while (missingIndexes.Count > 0)
                {
                    var hash = md5.ComputeHash(ENCODING.GetBytes(doorId + index.ToString()));
                    var result = string.Join("", (hash).Select(hashByte => hashByte.ToString("x2")));
                    if (result.StartsWith(PREFIX))
                    {
                        var digitIndex = result[5];
                        if (missingIndexes.Contains(digitIndex))
                        {
                            password[int.Parse(digitIndex.ToString())] = result[6];
                            missingIndexes.Remove(digitIndex);
                        }
                    }
                    index++;
                }
            return string.Join("", password);
        }

        static string GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim();
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
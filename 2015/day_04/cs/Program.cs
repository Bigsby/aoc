using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace AoC
{
    class Program
    {
        static int FindHash(string secretKey, int prefixCount)        
        {
            var prefix = new string('0', prefixCount);
            var guess = 1;
            using (var md5 = MD5.Create())
                while (true)
                {
                    var hash = md5.ComputeHash(UTF8Encoding.UTF8.GetBytes(secretKey + guess));
                    var result = string.Join("", (hash).Select(hashByte => hashByte.ToString("x2")));
                    if (result.StartsWith(prefix))
                        return guess;
                    guess += 1;
                }
        }

        static int Part1(string secretKey) => FindHash(secretKey, 5);

        static int Part2(string secretKey) => FindHash(secretKey, 6);

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
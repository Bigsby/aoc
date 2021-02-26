using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Security.Cryptography;
using System.Text;

namespace AoC
{
    class Program
    {
        static int FindHash(string secretKey, string prefix, int guess)
        {
            using (var md5 = MD5.Create())
                while (true)
                {
                    var hash = md5.ComputeHash(UTF8Encoding.UTF8.GetBytes(secretKey + guess));
                    var result = BitConverter.ToString(hash);
                    if (result.StartsWith(prefix))
                        return guess;
                    guess++;
                }
        }

        static (int, int) Solve(string secretKey)
        {
            var part1Result = FindHash(secretKey, "00-00-0", 1);
            return (part1Result, FindHash(secretKey, "00-00-00", part1Result));
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
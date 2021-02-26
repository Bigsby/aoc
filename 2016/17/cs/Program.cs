using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;
using System.Numerics;

namespace AoC
{
    static class Program
    {
        static IEnumerable<(int, char, Complex)> DIRECTIONS = new List<(int, char, Complex)> {
            ( 0, 'U', Complex.ImaginaryOne ),
            ( 1, 'D', -Complex.ImaginaryOne ),
            ( 2, 'L', -1 ),
            ( 3, 'R', 1 )
        };
        static Complex TARGET_ROOM = new Complex(3, -3);
        static Encoding ENCODING = UTF8Encoding.UTF8;
        static (string, int) Solve(string passcode)
        {
            var queue = new Queue<(Complex, string)>();
            queue.Enqueue((0, string.Empty));
            var shortestPath = string.Empty;
            var longestPathFound = 0;
            using (var md5 = MD5.Create())
                while (queue.Any())
                {
                    var (room, path) = queue.Dequeue();
                    if (room == TARGET_ROOM)
                    {
                        if (string.IsNullOrEmpty(shortestPath))
                            shortestPath = path;
                        longestPathFound = Math.Max(longestPathFound, path.Length);
                        continue;
                    }
                    var pathHash = string.Join("", md5.ComputeHash(ENCODING.GetBytes(passcode + path)).Select(hashByte => hashByte.ToString("x2")));
                    foreach (var (index, pathLetter, direction) in DIRECTIONS)
                    {
                        var newRoom = room + direction;
                        if (pathHash[index] > 'a' && newRoom.Real is >= 0 and < 4 && newRoom.Imaginary is > -4 and <= 0)
                            queue.Enqueue((newRoom, path + pathLetter));
                    }
                }
            return (shortestPath, longestPathFound);
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


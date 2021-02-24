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

        static string Part1(string passcode)
        {
            var queue = new Queue<(Complex, string)>();
            queue.Enqueue((0, string.Empty));
            using (var md5 = MD5.Create())
                while (queue.Any())
                {
                    var (room, path) = queue.Dequeue();
                    if (room == TARGET_ROOM)
                        return path;
                    var pathHash = string.Join("", md5.ComputeHash(ENCODING.GetBytes(passcode + path)).Select(hashByte => hashByte.ToString("x2")));
                    foreach (var (index, pathLetter, direction) in DIRECTIONS)
                    {
                        var newRoom = room + direction;
                        if (pathHash[index] > 'a' && newRoom.Real is >= 0 and < 4 && newRoom.Imaginary is > -4 and <= 0)
                            queue.Enqueue((newRoom, path + pathLetter));
                    }
                }
            throw new Exception("Path not found");
        }

        static int Part2(string passcode)
        {
            var queue = new Queue<(Complex, string)>();
            queue.Enqueue((0, string.Empty));
            var longestPathFound = 0;
            using (var md5 = MD5.Create())
                while (queue.Any())
                {
                    var (room, path) = queue.Dequeue();
                    if (room == TARGET_ROOM)
                    {
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
            return longestPathFound;
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


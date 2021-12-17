using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    static class Program
    {
        static bool IsDirectionValid((int, int, int, int) targetArea, (int, int) direction)
        {
            var (x1, x2, y1, y2) = targetArea;
            var (directionX, directionY) = direction;
            var currentX = 0;
            var currentY = 0;
            while (currentX <= x2 && currentY >= y1)
            {
                currentX += directionX;
                currentY += directionY;
                if (currentX >= x1 && currentX <= x2 && currentY >= y1 && currentY <= y2)
                    return true;
                directionX = directionX == 0 ? 0 : directionX - 1;
                directionY -= 1;
            }
            return false;
        }

        static int CountValidInRange((int, int, int, int) targetArea, int xStart, int xEnd, int yStart, int yEnd)
        {
            var count = 0;
            for (var x = xStart; x < xEnd; x++)
                for (var y = yStart; y < yEnd; y++)
                    if (IsDirectionValid(targetArea, (x, y)))
                        count++;
            return count;
        }

        static (int, int) Solve((int, int, int, int) targetArea)
        {
            var (x1, x2, y1, y2) = targetArea;
            var yDirection = -y1 - 1;
            var validDirectionCount = (x2 - x1 + 1) * (-y1 + y2 + 1);
            validDirectionCount += CountValidInRange(
                targetArea,
                (int)Math.Ceiling((Math.Sqrt(8 * x1 + 1) - 1) / 2), x2 / 2 + 2,
                y2 + 1, -y1
            );
            return ((yDirection * (yDirection + 1)) / 2, validDirectionCount);
        }

        static (int, int, int, int) GetInput(string filePath)
        { 
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var inputMatch = Regex.Match(File.ReadAllText(filePath), @"target area: x=(?<x1>-?\d+)..(?<x2>-?\d+), y=(?<y1>-?\d+)..(?<y2>-?\d+)");
            if (inputMatch.Success)
                return (
                    int.Parse(inputMatch.Groups["x1"].Value),
                    int.Parse(inputMatch.Groups["x2"].Value),
                    int.Parse(inputMatch.Groups["y1"].Value),
                    int.Parse(inputMatch.Groups["y2"].Value)
                );
            throw new Exception("Bad input");
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

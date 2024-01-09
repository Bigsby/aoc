using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<string>;

    record struct Lens(string Label, int FocalLength);

    static class Program
    {
        static int GetHashValue(string step)
        {
            var currentValue = 0;
            foreach (var c in step)
            {
                currentValue += (byte)c;
                currentValue *= 17;
                currentValue %= 256;
            }
            return currentValue;
        }

        static int Part2(Input puzzleInput)
        {
            var boxes = new List<Lens>[256];
            for (var index = 0; index < 256; index++)
                boxes[index] = new List<Lens>();
            foreach (var step in puzzleInput)
            {
                var oparationIndex = -1;
                var label = "";
                var length = -1;
                if ((oparationIndex = step.IndexOf("=", 0, step.Length)) != -1)
                {
                    label = step.Substring(0, oparationIndex);
                    length = int.Parse(step.Substring(oparationIndex + 1));
                }
                else 
                    label = step.Substring(0, step.Length - 1);
                var box = boxes[GetHashValue(label)];
                var existingLensIndex = box.FindIndex(lens => lens.Label == label);
                if (oparationIndex == -1)
                {
                    if (existingLensIndex != -1)
                        box.RemoveAt(existingLensIndex);
                }
                else 
                {
                    var newLens = new Lens(label, length);
                    if (existingLensIndex == -1)
                        box.Add(newLens);
                    else
                        box[existingLensIndex] = newLens;
                }
            }
            var result = 0;
            for (var index = 0; index < 256; index++)
                result += boxes[index].Select((lens, slot) => (index + 1) * (slot  + 1) * lens.FocalLength).Sum();
            return result;
        }

        static (int, int) Solve(Input puzzleInput)
            => (puzzleInput.Sum(step => GetHashValue(step)), Part2(puzzleInput));

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim().Split(",");

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

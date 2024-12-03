using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = String;

    static class Program
    {
        static int DoMultiplications(Input puzzleInput, bool enableSwitch)
        {
            var total = 0;
            var currentIndex = 0;
            var enabled = true;
            while (true)
            {
                var nextMulIndex = puzzleInput.IndexOf("mul", currentIndex);
                if (enableSwitch)
                {
                    var nextDoIndex = puzzleInput.IndexOf("do", currentIndex);
                    if (nextDoIndex != -1 && nextDoIndex < nextMulIndex)
                        switch(puzzleInput[nextDoIndex + 2])
                        {
                            case '(':
                                if (puzzleInput[nextDoIndex + 3] == ')')
                                {
                                    enabled = true;
                                    currentIndex = nextDoIndex + 4;
                                    continue;
                                }
                                break;
                            case 'n':
                                if (puzzleInput.Substring(nextDoIndex + 3, 4) == "'t()")
                                {
                                    enabled = false;
                                    currentIndex = nextDoIndex + 6;
                                    continue;
                                }
                                break;
                        }
                }
                if (nextMulIndex == -1)
                    break;
                currentIndex = nextMulIndex + 3;
                if (puzzleInput[currentIndex++] != '(')
                    continue;
                var numberIndex = currentIndex;
                while (char.IsDigit(puzzleInput[currentIndex++]));
                if (puzzleInput[currentIndex - 1] != ',')
                    continue;
                var firstValue = int.Parse(puzzleInput.Substring(numberIndex, currentIndex - numberIndex - 1));
                numberIndex = currentIndex;
                while (char.IsDigit(puzzleInput[currentIndex++]));
                if (puzzleInput[currentIndex - 1] != ')')
                    continue;
                if (enabled)
                    total += firstValue * int.Parse(puzzleInput.Substring(numberIndex, currentIndex - numberIndex - 1));
            }
            return total;
        }

        static (int, int) Solve(Input puzzleInput)
            => (DoMultiplications(puzzleInput, false), DoMultiplications(puzzleInput, true));

        static Input GetInput(string filePath)
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

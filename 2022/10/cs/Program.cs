using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<Tuple<OpCode, int>>;

    enum OpCode
    {
        AddX,
        NoOp
    }

    static class Program
    {
        const int CHARACTER_WIDTH = 5;
        const int CHARACTER_HEIGHT = 6;
        const int SCREEN_WIDTH = 40;
        static IDictionary<int, char> LETTERS = new Dictionary<int, char> {
            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b11110 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'A' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b11100 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b11100 << CHARACTER_WIDTH * 5), 'B' },

            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'C' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b11100 << CHARACTER_WIDTH * 5), 'D' },

            {   (0b11110 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b11100 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b11110 << CHARACTER_WIDTH * 5), 'E' },

            {   (0b11110 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b11100 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b10000 << CHARACTER_WIDTH * 5), 'F' },

            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b10110 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01110 << CHARACTER_WIDTH * 5), 'G' },

            {   (0b10010 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b11110 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'H' },

            {   (0b01110 << CHARACTER_WIDTH * 0) +
                (0b00100 << CHARACTER_WIDTH * 1) +
                (0b00100 << CHARACTER_WIDTH * 2) +
                (0b00100 << CHARACTER_WIDTH * 3) +
                (0b00100 << CHARACTER_WIDTH * 4) +
                (0b01110 << CHARACTER_WIDTH * 5), 'I' },

            {   (0b00110 << CHARACTER_WIDTH * 0) +
                (0b00010 << CHARACTER_WIDTH * 1) +
                (0b00010 << CHARACTER_WIDTH * 2) +
                (0b00010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'J' },

            {   (0b10010 << CHARACTER_WIDTH * 0) +
                (0b10100 << CHARACTER_WIDTH * 1) +
                (0b11000 << CHARACTER_WIDTH * 2) +
                (0b10100 << CHARACTER_WIDTH * 3) +
                (0b10100 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'K' },

            {   (0b10000 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b11110 << CHARACTER_WIDTH * 5), 'L' },

            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'O' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b11100 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b10000 << CHARACTER_WIDTH * 5), 'P' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b11100 << CHARACTER_WIDTH * 3) +
                (0b10100 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'R' },

            {   (0b01110 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b01100 << CHARACTER_WIDTH * 3) +
                (0b00010 << CHARACTER_WIDTH * 4) +
                (0b11100 << CHARACTER_WIDTH * 5), 'S' },

            {   (0b10010 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'U' },

            {   (0b10001 << CHARACTER_WIDTH * 0) +
                (0b10001 << CHARACTER_WIDTH * 1) +
                (0b01010 << CHARACTER_WIDTH * 2) +
                (0b00100 << CHARACTER_WIDTH * 3) +
                (0b00100 << CHARACTER_WIDTH * 4) +
                (0b00100 << CHARACTER_WIDTH * 5), 'Y' },

            {   (0b11110 << CHARACTER_WIDTH * 0) +
                (0b00010 << CHARACTER_WIDTH * 1) +
                (0b00100 << CHARACTER_WIDTH * 2) +
                (0b01000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b11110 << CHARACTER_WIDTH * 5), 'Z' }
        };

        static int Part1(Input instructions)
        { 
            var cycle = 0;
            var nextTestCycle = 20;
            var strengthsSum = 0;
            var registerX = 1;
            foreach (var (opCode, value) in instructions)
            {
                var instructionCycles = opCode == OpCode.NoOp ? 1 : 2;
                for (var i = 0; i < instructionCycles; i++)
                {
                    cycle++;
                    if (cycle == nextTestCycle)
                    {
                        strengthsSum += registerX * cycle;
                        nextTestCycle += SCREEN_WIDTH;
                    }
                }
                registerX += value;
            }
            return strengthsSum;
        }

        static char GetLetterInCRT(char[] crt, int index, int width, int height)
        {
            var screenValue = Enumerable.Range(0, height).SelectMany(y => Enumerable.Range(0, width).Select(x => (x, y)))
                .Where(pair => pair.x < width - 1 && crt[width * index + pair.x + pair.y * SCREEN_WIDTH] == '#')
                .Sum(pair => (int)Math.Pow(2, width - 1 - pair.x) << (pair.y * width));
            return LETTERS[screenValue];
        }

        static string Part2(Input instructions)
        {
            var crt = Enumerable.Repeat('.', SCREEN_WIDTH * CHARACTER_HEIGHT).ToArray();
            var cycle = 0;
            var registerX = 1;
            foreach (var (opCode, value) in instructions)
            {
                var instructionCycles = opCode == OpCode.NoOp ? 1 : 2;
                for (var i = 0; i < instructionCycles; i++)
                {
                    cycle++;
                    if (registerX <= cycle % SCREEN_WIDTH && cycle % SCREEN_WIDTH <= registerX + 2)
                        crt[cycle - 1] = '#';
                }
                registerX += value;
            }
            return string.Join("", Enumerable.Range(0, (SCREEN_WIDTH / CHARACTER_WIDTH)).Select(index =>
                GetLetterInCRT(crt, index, CHARACTER_WIDTH, CHARACTER_HEIGHT)));;
        }

        static (int, string) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => {
                var split = line.Split(" ");
                return split[0] == "addx" ? Tuple.Create(OpCode.AddX, int.Parse(split[1])) : Tuple.Create(OpCode.NoOp, 0);
            });

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

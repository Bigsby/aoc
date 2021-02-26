using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Instructions = IEnumerable<(InstructionType type, int a, int b)>;
    using Screen = IEnumerable<Complex>;
    enum InstructionType {
        Rect,
        RotateRow,
        RotateColumn
    }

    class Program
    {
        const int SCREEN_WIDTH = 50;
        const int SCREEN_HEIGTH = 6;
        const int CHARACTER_WIDTH = 5;
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

        static void PrintScreen(IEnumerable<Complex> screen, int width, int height)
        {
            foreach (var y in Enumerable.Range(0, height))
            {
                foreach (var x in Enumerable.Range(0, width))
                    Write(screen.Contains(new Complex(x, y)) ? '#' : '.');
                WriteLine();
            }
            WriteLine();
        }

        static Screen RunInstructions(Instructions instructions, int width, int height)
        {
            var screen = new List<Complex>();
            var toAdd = new List<Complex>();
            var toRemove = new List<Complex>();
            foreach (var (type, a, b) in instructions)
            {
                switch (type)
                {
                    case InstructionType.Rect:
                        foreach (var (x, y) in Enumerable.Range(0, a).SelectMany(x => Enumerable.Range(0, b).Select(y => (x, y))))
                        {
                            var position = new Complex(x, y);
                            if (!screen.Contains(position))
                                screen.Add(position);
                        }
                        break;
                    case InstructionType.RotateRow:
                        foreach (var position in screen.Where(p => p.Imaginary == a))
                        {
                            toRemove.Add(position);
                            toAdd.Add(new Complex((int)(position.Real + b) % width, (int)position.Imaginary));
                        }
                        break;
                    case InstructionType.RotateColumn:
                        foreach (var position in screen.Where(p => p.Real == a))
                        {
                            toRemove.Add(position);
                            toAdd.Add(new Complex((int)position.Real, (int)(position.Imaginary + b) % height));
                        }
                        break;
                }
                foreach (var position in toRemove)
                    screen.Remove(position);
                foreach (var position in toAdd)
                    screen.Add(position);
                toAdd.Clear();
                toRemove.Clear();
            }
            return screen;
        }

        static char GetCharacterInScreen(Screen screen, int index, int width, int height)
        {
            var screenValue = Enumerable.Range(0, height).SelectMany(y => Enumerable.Range(0, width).Select(x => (x, y)))
                .Where(pair => screen.Contains(new Complex(width * index + pair.x, pair.y)))
                .Sum(pair => (int)Math.Pow(2, width - 1 - pair.x) << (pair.y * width));
            return LETTERS[screenValue];
        }

        static (int, string) Solve(Instructions instructions)
        {
            var screen = RunInstructions(instructions, SCREEN_WIDTH, SCREEN_HEIGTH);
            return (
                screen.Count(), 
                new string(Enumerable.Range(0, SCREEN_WIDTH / CHARACTER_WIDTH)
                    .Select(index => 
                        GetCharacterInScreen(screen, index, CHARACTER_WIDTH, SCREEN_HEIGTH)
                    ).ToArray())
            );
        }

        static Instructions GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => {
                if (line.StartsWith("rect"))
                {
                    var ab = line[5..].Split('x');
                    return (InstructionType.Rect, int.Parse(ab[0]), int.Parse(ab[1]));
                }
                else if (line.StartsWith("rotate row"))
                {
                    var ya = line[13..].Split(" by ");
                    return (InstructionType.RotateRow, int.Parse(ya[0]), int.Parse(ya[1]));
                } else {
                    var xa = line[16..].Split(" by ");
                    return (InstructionType.RotateColumn, int.Parse(xa[0]), int.Parse(xa[1]));
                }
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
using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Numerics;
using System.Collections.Generic;

namespace AoC
{
    class Program
    {
        static Complex C(double real, double imaginary) => new Complex(real, imaginary);

        static Dictionary<char, Complex> DIRECTIONS = new Dictionary<char, Complex> {
            { 'U', C( 0, -1) },
            { 'D', C( 0,  1) },
            { 'L', C(-1,  0) },
            { 'R', C( 1,  0) }
        };
        static Tuple<Complex, char> GetButtonForPath(Complex position, string path, Dictionary<Complex, char> keypad)
        {
            foreach (var move in path)
            {
                var newPosition = position + DIRECTIONS[move];
                if (keypad.ContainsKey(newPosition))
                {
                    position = newPosition;
                }
            }
            return Tuple.Create(position, keypad[position]);
        }

        static string GetCode(string[] paths, Dictionary<Complex, char> keypad)
        {
            Complex position = 0;
            List<char> code = new List<char>();
            foreach (var path in paths)
            {
                var (newPosition, digit) = GetButtonForPath(position, path, keypad);
                position = newPosition;
                code.Add(keypad[position]);
            }
            return new string(code.ToArray());
        }

        static Dictionary<Complex, char> KEYPAD1 = new Dictionary<Complex, char> { 
            { C(-1, -1), '1' }, { C(0, -1), '2' }, { C(1, -1), '3' }, 
            { C(-1,  0), '4' }, { C(0,  0), '5' }, { C(1,  0), '6' }, 
            { C(-1,  1), '7' }, { C(0,  1), '8' }, { C(1,  1), '9' }, 
        };
        static string Part1(string[] paths)
        {
            return GetCode(paths, KEYPAD1);
        }

        static Dictionary<Complex, char> KEYPAD2 = new Dictionary<Complex, char> {
                                                 { C(0, -2), '1' },
                              { C(-1, -1), '2'}, { C(0, -1), '3'}, { C(1, -1), '2'},
            { C(-2, 0), '5'}, { C(-1,  0), '6'}, { C(0,  0), '7'}, { C(1,  0), '8'}, { C(2, 0), '9'},
                              { C(-1,  1), 'A'}, { C(0,  1), 'B'}, { C(1,  1), 'C'},
                                                 { C(0,  2), 'D'},
        };
        static string Part2(string[] paths)
        {
            return GetCode(paths, KEYPAD2);
        }

        static string[] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(line => line.Trim()).ToArray();
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
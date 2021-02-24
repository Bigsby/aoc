using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    class Program
    {
        const int IMAGE_WIDTH = 25;
        const int IMAGE_HEIGHT = 6;
        const int PIXELS_PER_LAYER = IMAGE_WIDTH * IMAGE_HEIGHT;
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

        static IEnumerable<int[]> GetImageLayers(IEnumerable<int> pixels)
        {
            var pixelsArray = pixels.ToArray();
            var layerCount = pixelsArray.Length / PIXELS_PER_LAYER;
            return Enumerable.Range(0, layerCount)
                .Select(layerIndex => pixelsArray[new Range(layerIndex * PIXELS_PER_LAYER, PIXELS_PER_LAYER * (layerIndex + 1))]);
        }

        static int Part1(IEnumerable<int> pixels)
        {
            var leastZeros = int.MaxValue;
            var result = 0;
            foreach (var layer in GetImageLayers(pixels))
            {
                var zeroCount = layer.Count(i => i == 0);
                if (zeroCount < leastZeros)
                {
                    leastZeros = zeroCount;
                    result = layer.Count(i => i == 1) * layer.Count(i => i == 2);
                }
            }
            return result;
        }

        const int WHITE = 1;
        const int TRANSPARENT = 2;

        static char GetCharacterInScreen(IDictionary<Complex, int> image, int index, int width, int height)
        {
            var screenValue = Enumerable.Range(0, height).SelectMany(y => Enumerable.Range(0, width).Select(x => (x, y)))
                .Where(pair => image[new Complex(width * index + pair.x, pair.y)] == WHITE)
                .Sum(pair => (int)Math.Pow(2, width - 1 - pair.x) << (pair.y * width));
            return LETTERS[screenValue];
        }

        static string Part2(IEnumerable<int> pixels)
        {
            var xys = Enumerable.Range(0, IMAGE_HEIGHT)
                .SelectMany(y => Enumerable.Range(0, IMAGE_WIDTH).Select(x => (x, y)));
            var image = xys.ToDictionary(pair => new Complex(pair.x, pair.y), _ => TRANSPARENT);
            foreach (var layer in GetImageLayers(pixels))
                foreach (var (x, y) in xys)
                {
                    var position = new Complex(x, y);
                    if (image[position] < 2)
                        continue;
                    image[position] = layer[x + y * IMAGE_WIDTH];
                }
            return new string(Enumerable.Range(0, IMAGE_WIDTH / CHARACTER_WIDTH).Select(index =>
                GetCharacterInScreen(image, index, CHARACTER_WIDTH, IMAGE_HEIGHT)
            ).ToArray());
        }

        static IEnumerable<int> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim().Select(c => int.Parse(c.ToString()));
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
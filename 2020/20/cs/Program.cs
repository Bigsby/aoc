using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Numerics;

namespace AoC
{
    using Tile = IEnumerable<Complex>;
    using Puzzle = Dictionary<Complex, IEnumerable<Complex>>;

    static class Program
    {
        static int GetSize(Tile tile, bool height = false)
            => height ? (int)tile.Max(p => p.Imaginary) : (int)tile.Max(p => p.Real);

        static void PrintTile(Tile tile)
        {
            var startX = (int)tile.Min(p => p.Real);
            var endX = (int)tile.Max(p => p.Real);
            var startY = (int)tile.Min(p => p.Imaginary);
            var endY = (int)tile.Max(p => p.Imaginary);
            for (var y = startY; y < endY + 1; y++)
            {
                for (var x = startX; x < endX + 1; x++)
                    Write(tile.Contains(new Complex(x, y)) ? '#' : '.');
                WriteLine();
            }
            WriteLine();
        }

        static Tile MirrorHorizontal(Tile tile, int size)
            => tile.Select(position => new Complex(size - position.Real, position.Imaginary));
        
        static Tile RotateClockwise(Tile tile, int size)
            => tile.Select(position => new Complex(size - position.Imaginary, position.Real));

        static IEnumerable<Tile> GeneratePermutations(Tile tile)
        {
            var size = GetSize(tile);
            foreach (var _ in Enumerable.Range(0, 4))
            {
                yield return tile;
                yield return MirrorHorizontal(tile, size);
                tile = RotateClockwise(tile, size);
            }
        }

        static Dictionary<int, Tile[]> GenerateAllTilesPermutations(IEnumerable<(int number, Tile tile)> tiles)
            => tiles.ToDictionary(pair => pair.number, pair => GeneratePermutations(pair.tile).ToArray());
        
        static Complex I = Complex.ImaginaryOne;
        static Dictionary<Complex, (Complex, Complex, Complex)> TESTS = new Dictionary<Complex, (Complex, Complex, Complex)> {
            { -I, (0, I, 1) },
            {  1, (1, 0, I) },
            {  I, (I, 0, 1) },
            {  -1, (0, 1, I) }
        };
        static bool TestSides(Tile tileA, Tile tileB, Complex side, int size)
        {
            var (positionAStart, positionBStart, step) = TESTS[side];
            var positionA = positionAStart * size;
            var positionB = positionBStart * size;
            foreach (var _ in Enumerable.Range(0, size + 1))
            {
                if (tileA.Contains(positionA) ^ tileB.Contains(positionB))
                    return false;
                positionA += step;
                positionB += step;
            }
            return true;
        }

        static (bool, Complex) DoPermutationsMatch(Tile permutationA, Tile permutationB, int size, IEnumerable<Complex> sides)
        {
            foreach (var side in sides)
                if (TestSides(permutationA, permutationB, side, size))
                    return (true, side);
            return (false, 0);
        }

        static (bool, Complex, Tile) DoTilesMatch(Tile tileA, IEnumerable<Tile> permutations, int size, IEnumerable<Complex> sides = null)
        {
            sides ??= TESTS.Keys;
            foreach (var permutation in permutations)
            {
                var (matched, side) = DoPermutationsMatch(tileA, permutation, size, sides);
                if (matched)
                    return (true, side, permutation);
            }
            return (false, 0, null);
        }

        static Complex[] GetMatchingSides((int, Tile) tile, IEnumerable<(int, Tile)> tiles, int size, Dictionary<int, Tile[]> allPermutations)
        {
            var (number, thisTile) = tile;
            var matchedSides = new List<Complex>();
            foreach (var (otherNumber, _) in tiles)
            {
                if (otherNumber == number)
                    continue;
                var (matched, side, _) = DoTilesMatch(thisTile, allPermutations[otherNumber], size);
                if (matched)
                    matchedSides.Add(side);
            }
            return matchedSides.ToArray();
        }

        static IEnumerable<(int number, Complex[] sides)> GetCorners(IEnumerable<(int number, Tile tile)> tiles, int size, Dictionary<int, Tile[]> allPermutations)
        {
            var tilesMatchesSides = tiles.ToDictionary(pair => pair.number, pair => GetMatchingSides(pair, tiles, size, allPermutations));
            return tilesMatchesSides.Where(pair => pair.Value.Count() == 2).Select(pair => (pair.Key, pair.Value));
        }

        static long Part1(IEnumerable<(int, Tile tile)> tiles)
        {
            var permutations = GenerateAllTilesPermutations(tiles);
            var size = GetSize(tiles.First().tile);
            return GetCorners(tiles, size, permutations).Aggregate(1L, (soFar, current) => soFar * current.number);
        }

        static Puzzle BuildPuzzle(IEnumerable<(int number, Tile tile)> tiles, int tileSize)
        {
            var tilePermutations = GenerateAllTilesPermutations(tiles);
            var (firstCornerNumber, sides) = GetCorners(tiles, tileSize, tilePermutations).First();
            var (sideOne, sideTwo) = (sides[0], sides[1]);
            var puzzleWidth = (int)Math.Sqrt(tiles.Count());
            var puzzlePosition = (puzzleWidth - 1) * ((sideOne == -1 || sideTwo == -1 ? 1 : 0) + (sideOne == -I || sideTwo == -I ? I : 0));
            var lastTile = tilePermutations[firstCornerNumber].First();
            tilePermutations.Remove(firstCornerNumber);
            var puzzle = new Puzzle();
            puzzle[puzzlePosition] = lastTile;
            var direction = sideOne;
            while (tilePermutations.Any())
            {
                puzzlePosition += direction;
                foreach (var (tileNumber, permutations) in tilePermutations.Select(pair => (pair.Key, pair.Value)))
                {
                    var (matched, _, matchedPermutation) = DoTilesMatch(lastTile, permutations, tileSize, new [] { direction });
                    if (matched)
                    {
                        puzzle[puzzlePosition] = lastTile = matchedPermutation;
                        tilePermutations.Remove(tileNumber);
                        if (direction == sideTwo)
                            direction = ((puzzle.Count / puzzleWidth) % 2 != 0 ? -1 : 1) * sideOne;
                        else if (puzzle.Count % puzzleWidth == 0)
                            direction = sideTwo;
                        break;
                    }
                }
            }
            return puzzle;
        }

        static Tile RemoveBordersAndJoin(Puzzle puzzle, int tileSize)
        {
            var offsetFactor = tileSize - 1;
            var reduced = new List<Complex>();
            foreach (var (puzzlePosition, tile) in puzzle.Select(pair => (pair.Key, pair.Value)))
                foreach (var position in tile)
                    if (position.Real > 0 && position.Real < tileSize && position.Imaginary > 0 && position.Imaginary < tileSize)
                        reduced.Add(new Complex(puzzlePosition.Real * offsetFactor + position.Real - 1, puzzlePosition.Imaginary * offsetFactor + position.Imaginary - 1));
            return reduced;
        }

        static string[] SEA_MONSTER = new [] {
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   "
        };
        static Tile GetSeaMonster()
        {
            var seaMonster = new List<Complex>();
            foreach (var (line, y) in SEA_MONSTER.Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                    if (c == '#')
                        seaMonster.Add(new Complex(x, y));
            return seaMonster;
        }

        static bool IsMonsterInLocation(Complex location, Tile puzzle, Tile seaMonster)
        
        {
            foreach (var monsterPosition in seaMonster)
                if (!puzzle.Contains(monsterPosition + location))
                    return false;
            return true;
        }

        static int GetSeaMonsterCount(Tile puzzle, Tile seaMonster)
        {
            var seaMonsterWidth = GetSize(seaMonster) + 1;
            var seaMonsterHeight = GetSize(seaMonster, true) + 1;
            var puzzleSize = GetSize(puzzle) + 1;
            foreach (var permutation in GeneratePermutations(puzzle))
            {
                var count = 0;
                for (var puzzleX = 0; puzzleX < puzzleSize - seaMonsterWidth; puzzleX++)
                    for (var puzzleY = 0; puzzleY < puzzleSize - seaMonsterHeight; puzzleY++)
                        if (IsMonsterInLocation(new Complex(puzzleX, puzzleY), permutation, seaMonster))
                            count++;
                if (count > 0)
                    return count;
            }
            return 0;
        }

        static int Part2(IEnumerable<(int, Tile tile)> tiles)
        {
            var tileSize = GetSize(tiles.First().tile);
            var puzzle = BuildPuzzle(tiles, tileSize);
            var reduced = RemoveBordersAndJoin(puzzle, tileSize);
            var seaMonster = GetSeaMonster();
            var locationCount = GetSeaMonsterCount(reduced, seaMonster);
            return reduced.Count() - (seaMonster.Count() * locationCount);

        }

        static Regex numberLineRegex = new Regex(@"^Tile\s(?<number>\d+):$", RegexOptions.Compiled);
        static IEnumerable<(int, Tile)> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var tiles = new List<(int, Tile)>();
            var tileNumber = 0;
            var tile = new List<Complex>();
            var position = Complex.Zero;
            foreach (var line in File.ReadLines(filePath))
            {
                var numberMatch = numberLineRegex.Match(line);
                if (numberMatch.Success)
                {
                    tileNumber = int.Parse(numberMatch.Groups["number"].Value);
                    tile = new List<Complex>();
                    position = Complex.Zero;
                }
                else if (string.IsNullOrEmpty(line.Trim()))
                    tiles.Add((tileNumber, tile));
                else
                {
                    foreach (var c in line.Trim())
                    {
                        if (c == '#')
                            tile.Add(position);
                        position += 1;
                    }
                    position = new Complex(0, position.Imaginary + 1);
                }
            }


            return tiles;
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

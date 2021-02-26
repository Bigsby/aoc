using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Walls = IEnumerable<Complex>;
    using Team = Dictionary<Complex,int>;

    class Program
    {
        static Complex[] ATTACK_DIRECTIONS = new [] { Complex.ImaginaryOne, -1, 1, -Complex.ImaginaryOne };

        static void DrawGame(Walls walls, Team elves, Team goblins)
        {
            var maxX = (int)walls.Max(w => w.Real);
            var minY = (int)walls.Min(w => w.Imaginary);
            for (var y = 0; y > minY - 1; y--)
            {
                for (var x = 0; x < maxX + 1; x++)
                {
                    var c = '.';
                    var position = new Complex(x, y);
                    if (walls.Contains(position))
                        c = '#';
                    else if (elves.ContainsKey(position))
                        c = 'E';
                    else if (goblins.ContainsKey(position))
                        c = 'G';
                    Write(c);
                }
                WriteLine();
            }
            WriteLine();
        }

        static IEnumerable<Complex> GetAttackPositions(Team mates, Team enemies, Walls walls)
        {
            var attackPositions = new HashSet<Complex>();
            foreach (var enemy in enemies.Keys)
                foreach (var direction in ATTACK_DIRECTIONS)
                {
                    var attackPosition = enemy + direction;
                    if (!mates.ContainsKey(attackPosition) 
                        && !enemies.ContainsKey(attackPosition) 
                        && !walls.Contains(attackPosition))
                        attackPositions.Add(attackPosition);
                }
            return attackPositions.OrderBy(p => p.Imaginary).ThenBy(p => p.Real);
        }

        static bool Attack(Complex unitPosition, Team enemies, int attackPower)
        {
            var targets = new List<(int hitPoints, Complex position)>();
            foreach (var direction in ATTACK_DIRECTIONS)
            {
                var enemyPosition = unitPosition + direction;
                if (enemies.ContainsKey(enemyPosition))
                    targets.Add((enemies[enemyPosition], enemyPosition));
            }
            if (targets.Any())
            {
                var target = targets.OrderBy(t => t.hitPoints)
                    .ThenBy(t => -t.position.Imaginary)
                    .ThenBy(t => t.position.Real).First();
                enemies[target.position] -= attackPower;
                if (enemies[target.position] <= 0)
                    enemies.Remove(target.position);
                return true;
            }
            return false;
        }

        static Complex[] MOVE_DIRECTIONS = new [] { -Complex.ImaginaryOne, Complex.ImaginaryOne, -1, 1 };
        static Complex GetMove(Complex start, IEnumerable<Complex> targets, Walls invalidPositions)
        {
            var firstMoves = MOVE_DIRECTIONS.Select(direction => start + direction)
                .Where(p => !invalidPositions.Contains(p));
            var bestMoves = new List<(Complex firstMove, int length, Complex destination)>();
            foreach (var move in firstMoves)
            {
                if (targets.Contains(move))
                {
                    bestMoves.Add((move, 1, move));
                    continue;
                }
                var seenPositions = new List<Complex>();
                seenPositions.Add(start);
                seenPositions.Add(move);
                var stack = MOVE_DIRECTIONS
                    .Select(direction => move + direction)
                    .Where(p => !invalidPositions.Contains(p));
                var length = 1;
                var run = true;
                while (run)
                {
                    length += 1;
                    var newStack = new List<Complex>();
                    foreach (var newPosition in stack)
                    {
                        if (seenPositions.Contains(newPosition))
                            continue;
                        seenPositions.Add(newPosition);
                        if (targets.Contains(newPosition))
                        {
                            bestMoves.Add((move, length, newPosition));
                            run = false;
                            continue;
                        }
                        newStack.AddRange(MOVE_DIRECTIONS.Select(direction => newPosition + direction).Where(p =>
                            !seenPositions.Contains(p) && !invalidPositions.Contains(p)
                        ));
                    }
                    stack = newStack.ToList();
                    if (!stack.Any())
                        run = false;
                }
            }
            if (!bestMoves.Any())
                return -1;
            var minLength = bestMoves.Min(m => m.length);
            return bestMoves.Where(m => m.length == minLength)
                .OrderBy(m => -m.destination.Imaginary).ThenBy(m => m.destination.Real)
                .ThenBy(m => -m.firstMove.Imaginary).ThenBy(m => m.firstMove.Real).First().firstMove;
        }

        static Complex MakeUnitTurn(Complex unitPosition, Team mates, Team enemies, Walls walls, int attackPower)
        {
            if (Attack(unitPosition, enemies, attackPower))
                return unitPosition;
            var attackPositions = GetAttackPositions(mates, enemies, walls);
            var wholeMap = walls.Concat(mates.Keys).Concat(enemies.Keys);
            var newPosition = GetMove(unitPosition, attackPositions, wholeMap);
            if (newPosition != -1)
            {
                var hitPoints = mates[unitPosition];
                mates.Remove(unitPosition);
                mates[newPosition] = hitPoints;
                Attack(newPosition, enemies, attackPower);
                return newPosition;
            }
            return unitPosition;
        }

        const int DEFAULT_POWER = 3;

        static bool MakeRound(Walls walls, Team elves, Team goblins, int elfPower)
        {
            var unitsToPlay = new Queue<Complex>(elves.Keys.Concat(goblins.Keys).OrderBy(p => -p.Imaginary).ThenBy(p => p.Real));
            var newPositions = new List<Complex>();
            while (unitsToPlay.Any())
            {
                var position = unitsToPlay.Dequeue();
                if (newPositions.Contains(position))
                    continue;
                var newPosition = -Complex.One;
                if (goblins.ContainsKey(position))
                {
                    if (!elves.Any())
                        return false;
                    newPosition = MakeUnitTurn(position, goblins, elves, walls, DEFAULT_POWER);
                    newPositions.Add(newPosition);
                } else if (elves.ContainsKey(position))
                {
                    if (!goblins.Any())
                        return false;
                    newPosition = MakeUnitTurn(position, elves, goblins, walls, elfPower);
                    newPositions.Add(newPosition);
                }
            }
            return true;
        }

        static (bool success, int score) RunGame(Walls walls, Team elves, Team goblins, bool allElves, int elfPower = DEFAULT_POWER)
        {
            elves = new Dictionary<Complex, int>(elves);
            var startingElves = elves.Count;
            goblins = new Dictionary<Complex, int>(goblins);
            var round = 0;
            while (MakeRound(walls, elves, goblins, elfPower) && !(allElves && elves.Count != startingElves))
                round++;
            return (elves.Count == startingElves, round * (elves.Values.Sum() + goblins.Values.Sum()));
        }

        static int Part1((Walls walls, Team elves, Team goblins) game)
            => RunGame(game.walls, game.elves, game.goblins, false).score;

        static int Part2((Walls walls, Team elves, Team goblins) game)
        {
            var (walls, elves, goblins) = game;
            var success = false;
            var elfPower = 10;
            var result = 0;
            while (true)
            {
                (success, result) = RunGame(walls, elves, goblins, true, ++elfPower);
                if (success)
                    return result;
            }
        }

        static (int, int) Solve((Walls walls, Team elves, Team goblins) game)
            => (
                RunGame(game.walls, game.elves, game.goblins, false).score,
                Part2(game)
            );

        const char WALL = '#';
        const char ELF = 'E';
        const char GOBLIN = 'G';
        const int STARTING_HITPOINTS = 200;
        static (Walls walls, Team elves, Team goblins) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);

            var walls = new List<Complex>();
            var elves = new Team();
            var goblins = new Team();
            foreach (var (line, y) in File.ReadLines(filePath).Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                {
                    var position = new Complex(x, -y);
                    if (c == WALL)
                        walls.Add(position);
                    else if (c == ELF)
                        elves[position] = STARTING_HITPOINTS;
                    else if (c == GOBLIN)
                        goblins[position] = STARTING_HITPOINTS;
                }
            return ((IEnumerable<Complex>)walls, elves, goblins);
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
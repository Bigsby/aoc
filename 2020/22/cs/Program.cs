using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    class Player
    {
        public string Name { get; init; }
        public int LastCard { get; private set; }
        public bool HasCards => _cards.Any();
        public int Count => _cards.Count;
        public bool LastCardSmaller => LastCard <= Count;

        public Player(string name, IEnumerable<int> cards)
        {
            Name = name;
            _cards = new Queue<int>(cards);
        }

        public int GetTopCard()
        {
            _previousHands.Add(_cards.ToArray());
            return LastCard = _cards.Dequeue();
        }

        public void AddCards(int card1, int card2)
        {
            _cards.Enqueue(card1);
            _cards.Enqueue(card2);
        }

        public bool HasRepeatedHand()
            => _previousHands.Any(previous => !_cards.Except(previous).Any() && ! previous.Except(_cards).Any());

        public int GetScore()
        {
            var worth = 1;
            return _cards.Reverse().Sum(card => card * worth++);
        }

        public Player Clone(bool keepState = false)
        {
            if (keepState)
                return new Player(Name, _cards.Take(LastCard).ToArray());
            return new Player(Name, _cards);
        }

        public static Player FromLines(string lines)
        {
            var splits = lines.Split("\n", options: StringSplitOptions.RemoveEmptyEntries);
            var name = splits[0].Replace("Player", "").Replace(":", "");
            return new Player(name, splits[1..].Select(line => int.Parse(line.Trim())));
        }

        public override string ToString()
            => $"{Name}: {string.Join(',', _cards)}";

        private Queue<int> _cards;
        private List<int[]> _previousHands = new List<int[]>();
    }

    static class Program
    {
        static (Player, Player) GetPlayersFromInput((Player player1, Player player2) players)
            => (players.player1.Clone(), players.player2.Clone());

        static int Part1((Player, Player) players)
        {
            var (player1, player2) = GetPlayersFromInput(players);
            while (player1.HasCards && player2.HasCards)
            {
                var player1Card = player1.GetTopCard();
                var player2Card = player2.GetTopCard();
                if (player1Card > player2Card)
                    player1.AddCards(player1Card, player2Card);
                else
                    player2.AddCards(player2Card, player1Card);
            }
            var winner = player1.HasCards ? player1 : player2;
            return winner.GetScore();
        }

        static (Player, Player) DecideRound (Player player1, Player player2)
        {
            if (player1.LastCardSmaller && player2.LastCardSmaller)
            {
                var winner = PlayGame(player1.Clone(true), player2.Clone(true));
                if (winner.Name == player1.Name)
                    return (player1, player2);
                return (player2, player1);
            } 
            else
            {
                if (player1.LastCard > player2.LastCard)
                    return (player1, player2);
                return (player2, player1);
            }
        }

        static Player PlayGame(Player player1, Player player2)
        {
            while (player1.HasCards && player2.HasCards)
            {
                if (player1.HasRepeatedHand() || player2.HasRepeatedHand())
                    return player1;
                player1.GetTopCard();
                player2.GetTopCard();
                var (winner, looser) = DecideRound(player1, player2);
                winner.AddCards(winner.LastCard, looser.LastCard);
            }
            return player1.HasCards ? player1 : player2;
        }

        static int Part2((Player, Player) players)
        {
            var (player1, player2) = GetPlayersFromInput(players);
            var winner = PlayGame(player1, player2);
            return winner.GetScore();
        }

        static (Player, Player) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var split = File.ReadAllText(filePath).Split(Environment.NewLine + Environment.NewLine);
            return (Player.FromLines(split[0]), Player.FromLines(split[1]));
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

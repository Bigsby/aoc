use core::cell::RefCell;
use std::collections::VecDeque;
use std::fmt::Debug;

type Card = usize;
struct Player {
    number: usize,
    cards: RefCell<VecDeque<Card>>,
    previous_hands: RefCell<Vec<VecDeque<Card>>>,
    last_card: Card,
}

impl Debug for Player {
    fn fmt(
        &self,
        formatter: &mut std::fmt::Formatter<'_>,
    ) -> std::result::Result<(), std::fmt::Error> {
        formatter
            .debug_struct("")
            .field("number", &self.number)
            .field("cards", &self.cards)
            .finish()
    }
}

impl Player {
    fn new(number: usize, cards: &Vec<Card>) -> Player {
        Player {
            number,
            last_card: 0,
            previous_hands: RefCell::new(Vec::new()),
            cards: RefCell::new(cards.iter().copied().collect()),
        }
    }

    fn from_lines(lines: &str) -> Player {
        let split = lines.split("\n").collect::<Vec<&str>>();
        let number = split[0][7..8].parse().unwrap();
        let cards = split[1..]
            .iter()
            .filter(|line| !line.is_empty())
            .map(|line| line.parse::<Card>().unwrap())
            .collect();
        Player::new(number, &cards)
    }

    fn get_top_card(&mut self) -> Card {
        let card = self.cards.borrow_mut().pop_front().unwrap();
        self.last_card = card;
        card
    }

    fn add_cards(&mut self, first: Card, second: Card) {
        self.cards.borrow_mut().push_back(first);
        self.cards.borrow_mut().push_back(second);
    }

    fn last_card_smaller(&self) -> bool {
        self.last_card <= self.cards.borrow().len()
    }

    fn has_repeated_hand(&self) -> bool {
        let current_hand: VecDeque<Card> = self.cards.borrow().iter().copied().collect();
        self.previous_hands
            .borrow()
            .iter()
            .any(|previous| previous == &current_hand)
    }

    fn has_cards(&self) -> bool {
        !self.cards.borrow().is_empty()
    }

    fn clone(&self, keep_state: bool) -> Player {
        if keep_state {
            Player::new(
                self.number,
                &self
                    .cards
                    .borrow()
                    .iter()
                    .take(self.last_card)
                    .copied()
                    .collect(),
            )
        } else {
            Player::new(self.number, &self.cards.borrow().iter().copied().collect())
        }
    }

    fn get_score(&self) -> usize {
        self.cards
            .borrow()
            .iter()
            .rev()
            .enumerate()
            .map(|(factor, card)| *card * (factor + 1))
            .sum()
    }
}

fn get_players_from_input(players: &(Player, Player)) -> (Player, Player) {
    (players.0.clone(false), players.1.clone(false))
}

fn _pause() {
    std::io::stdin().read_line(&mut String::new()).expect("");
}

fn part1(players: &(Player, Player)) -> usize {
    let (mut player1, mut player2) = get_players_from_input(players);
    while player1.has_cards() && player2.has_cards() {
        let player1_card = player1.get_top_card();
        let player2_card = player2.get_top_card();
        if player1_card > player2_card {
            player1.add_cards(player1_card, player2_card);
        } else {
            player2.add_cards(player2_card, player1_card);
        }
    }
    if player1.has_cards() {
        player1.get_score()
    } else {
        player2.get_score()
    }
}

fn play_game(player1: &mut Player, player2: &mut Player, round_decider: bool) -> usize {
    if round_decider {
        if player1.last_card_smaller() && player2.last_card_smaller() {
            return play_game(&mut player1.clone(true), &mut player2.clone(true), false);
        } else {
            if player1.last_card > player2.last_card {
                player1.number
            } else {
                player2.number
            }
        }
    } else {
        while player1.has_cards() && player2.has_cards() {
            if player1.has_repeated_hand() || player2.has_repeated_hand() {
                return player1.number;
            }
            player1.get_top_card();
            player2.get_top_card();
            let winner = play_game(player1, player2, true);
            if winner == player1.number {
                player1.add_cards(player1.last_card, player2.last_card);
            } else {
                player2.add_cards(player2.last_card, player1.last_card);
            }
        }
        if player1.has_cards() {
            player1.number
        } else {
            player2.number
        }
    }
}

fn part2(players: &(Player, Player)) -> usize {
    let (mut player1, mut player2) = get_players_from_input(players);
    if play_game(&mut player1, &mut player2, false) == player1.number {
        player1.get_score()
    } else {
        player2.get_score()
    }
}

fn solve(players: &(Player, Player)) -> (usize, usize) {
    (part1(players), part2(players))
}

fn get_input(file_path: &String) -> (Player, Player) {
    let splits: Vec<String> = std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split("\n\n")
        .map(|s| String::from(s))
        .collect();
    (
        Player::from_lines(&splits[0]),
        Player::from_lines(&splits[1]),
    )
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        panic!("Please, add input file path as parameter");
    }
    let now = std::time::Instant::now();
    let (part1_result, part2_result) = solve(&get_input(&args[1]));
    let end = now.elapsed().as_secs_f32();
    println!("P1: {}", part1_result);
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}

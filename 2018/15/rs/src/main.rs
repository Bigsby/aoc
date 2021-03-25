use num::complex::Complex;
use std::collections::{HashMap, HashSet};

type Position = Complex<i32>;
type Walls = Vec<Position>;
type Team = HashMap<Position, i32>;
const WALL: char = '#';
const ELF: char = 'E';
const GOBLIN: char = 'G';
const STARTING_HITPOINTS: i32 = 200;
const DEFAULT_POWER: i32 = 3;

fn _draw_game(walls: &Walls, elves: &Team, goblins: &Team) {
    print!("{}", 27 as char);
    print!("[2J");
    let max_x = walls.into_iter().map(|w| w.re).max().unwrap();
    let max_y = walls.into_iter().map(|w| w.im).max().unwrap();
    for y in 0..max_y + 1 {
        for x in 0..max_x + 1 {
            let position = Position::new(x, y);
            let mut c = '.';
            if walls.contains(&position) {
                c = WALL;
            } else if elves.contains_key(&position) {
                c = ELF;
            } else if goblins.contains_key(&position) {
                c = GOBLIN;
            }
            print!("{}", c);
        }
        println!();
    }
    println!("{:?}", elves);
    println!("{:?}", goblins);
    println!();
}

static ATTACK_DIRECTIONS: &'static [Position; 4] = &[
    Position::new(0, -1),
    Position::new(-1, 0),
    Position::new(1, 0),
    Position::new(0, 1),
];
fn get_attack_positions(enemies: &Team, invalid_positions: &Walls) -> Vec<Position> {
    let mut attack_positions = HashSet::new();
    for enemy in enemies.keys() {
        for direction in ATTACK_DIRECTIONS {
            let attack_position = enemy + direction;
            if !invalid_positions.contains(&attack_position) {
                attack_positions.insert(attack_position);
            }
        }
    }
    attack_positions.into_iter().collect()
}

fn attack(unit_position: &Position, enemies: &mut Team, attack_power: i32) -> bool {
    let mut targets = Vec::new();
    for direction in ATTACK_DIRECTIONS {
        let enemy_position = unit_position + direction;
        if let Some(hit_points) = enemies.get(&enemy_position) {
            targets.push((hit_points, enemy_position));
        }
    }
    if !targets.is_empty() {
        targets.sort_by_key(|t| (t.0, t.1.im, t.1.re));
        let target_position = targets[0].1;
        *enemies.get_mut(&target_position).unwrap() -= attack_power;
        if *enemies.get(&target_position).unwrap() <= 0 {
            enemies.remove_entry(&target_position);
        }
        return true;
    }
    false
}

static MOVE_DIRECTIONS: &'static [Position; 4] = &[
    Position::new(0, 1),
    Position::new(0, -1),
    Position::new(-1, 0),
    Position::new(1, 0),
];
fn get_move(
    start: Position,
    targets: &Vec<Position>,
    invalid_positions: &Walls,
) -> Option<Position> {
    let mut best_moves = Vec::new();
    let mut seen_positions: HashSet<Position> = HashSet::new();
    let mut min_length = i32::MAX;
    for move_ in MOVE_DIRECTIONS
        .iter()
        .map(|direction| start + direction)
        .filter(|x| !invalid_positions.contains(&x))
    {
        if targets.contains(&move_) {
            best_moves.push((move_, 1, move_))
        }
        seen_positions.clear();
        seen_positions.insert(start);
        seen_positions.insert(move_);
        let mut stack: Vec<Position> = MOVE_DIRECTIONS
            .iter()
            .map(|direction| move_ + direction)
            .filter(|p| !invalid_positions.contains(&p) && *p != start)
            .collect();
        let mut length = 1;
        'outer: loop {
            length += 1;
            let mut new_stack = Vec::new();
            for new_position in stack {
                if seen_positions.insert(new_position) {
                    if targets.contains(&new_position) {
                        min_length = length;
                        best_moves.push((move_, length, new_position));
                        break 'outer;
                    }
                }
                if length < min_length {
                    new_stack.extend(
                        MOVE_DIRECTIONS
                            .iter()
                            .map(|direcion| direcion + new_position)
                            .filter(|p| {
                                !invalid_positions.contains(p) && !seen_positions.contains(p)
                            }),
                    );
                }
            }
            stack = new_stack;
            if stack.is_empty() {
                break;
            }
        }
    }
    if best_moves.is_empty() {
        return None;
    }
    best_moves.sort_by_key(|m| (m.1, m.2.im, m.2.re, m.0.im, m.0.re));
    Some(best_moves[0].0)
}

fn make_unit_turn(
    unit_position: &Position,
    mates: &mut Team,
    enemies: &mut Team,
    walls: &Walls,
    attack_power: i32,
) -> Position {
    if attack(unit_position, enemies, attack_power) {
        return *unit_position;
    }
    let mut whole_map = mates.keys().map(|p| *p).collect::<Vec<Position>>();
    let attack_positions = get_attack_positions(enemies, &whole_map);
    whole_map.extend(enemies.keys().map(|p| *p));
    whole_map.extend(walls);
    if let Some(new_position) = get_move(*unit_position, &attack_positions, &whole_map) {
        let hit_points = *mates.get(unit_position).unwrap();
        mates.remove_entry(unit_position);
        mates.insert(new_position, hit_points);
        attack(&new_position, enemies, attack_power);
        return new_position;
    }
    *unit_position
}

fn make_round(walls: &Walls, elves: &mut Team, goblins: &mut Team, elf_power: i32) -> bool {
    let mut units_to_play: Vec<Position> = elves.keys().map(|p| *p).collect();
    units_to_play.extend(goblins.keys().map(|p| *p));
    units_to_play.sort_by_key(|p| (-p.im, -p.re));
    let mut new_positions = Vec::new();
    while let Some(position) = units_to_play.pop() {
        if new_positions.contains(&position) {
            continue;
        }
        if goblins.contains_key(&position) {
            if elves.is_empty() {
                return false;
            }
            new_positions.push(make_unit_turn(
                &position,
                goblins,
                elves,
                walls,
                DEFAULT_POWER,
            ));
        } else if elves.contains_key(&position) {
            if goblins.is_empty() {
                return false;
            }
            new_positions.push(make_unit_turn(&position, elves, goblins, walls, elf_power));
        }
    }
    true
}

fn run_game(
    walls: &Walls,
    elves: &Team,
    goblins: &Team,
    all_elves: bool,
    elf_power: i32,
) -> (bool, i32) {
    let starting_elves = elves.len();
    let mut round = 0;
    let mut elves: Team = elves.into_iter().map(|(k, v)| (*k, *v)).collect();
    let mut goblins: Team = goblins.into_iter().map(|(k, v)| (*k, *v)).collect();
    while make_round(walls, &mut elves, &mut goblins, elf_power)
        && !(all_elves && elves.len() != starting_elves)
    {
        round += 1;
    }
    (
        elves.len() == starting_elves,
        round * (elves.values().sum::<i32>() + goblins.values().sum::<i32>()),
    )
}

fn part1(game: &(Walls, Team, Team)) -> i32 {
    let (walls, elves, goblins) = game;
    run_game(walls, elves, goblins, false, DEFAULT_POWER).1
}

fn part2(game: &(Walls, Team, Team)) -> i32 {
    let (walls, elves, goblins) = game;
    let mut elf_power = 10;
    loop {
        elf_power += 1;
        let (success, result) = run_game(walls, elves, goblins, true, elf_power);
        if success {
            return result;
        }
    }
}

fn solve(game: &(Walls, Team, Team)) -> (i32, i32) {
    (part1(game), part2(game))
}

fn get_input(file_path: &String) -> (Walls, Team, Team) {
    let mut walls = Walls::new();
    let mut elves = Team::new();
    let mut goblins = Team::new();
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            let position = Position::new(x as i32, y as i32);
            if c == WALL {
                walls.push(position);
            } else if c == ELF {
                elves.insert(position, STARTING_HITPOINTS);
            } else if c == GOBLIN {
                goblins.insert(position, STARTING_HITPOINTS);
            }
        }
    }
    (walls, elves, goblins)
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

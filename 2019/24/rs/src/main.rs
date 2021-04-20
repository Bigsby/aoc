use num::Complex;
use std::collections::{HashMap, HashSet};

type Bug = Complex<i32>;
type Bugs = Vec<Bug>;
type LayeredBugs = HashMap<i32, Bugs>;
static DIRECTIONS: &'static [Bug] = &[
    Bug::new(1, 0),
    Bug::new(-1, 0),
    Bug::new(0, 1),
    Bug::new(0, -1),
];

fn gets_bug(has_bug: bool, adjacent_count: usize) -> bool {
    if has_bug {
        adjacent_count == 1
    } else {
        adjacent_count == 1 || adjacent_count == 2
    }
}

fn next_minute(bugs: &Bugs) -> Bugs {
    let mut new_state = Bugs::new();
    for y in 0..5 {
        for x in 0..5 {
            let position = Bug::new(x, y);
            let adjacent_count = DIRECTIONS
                .iter()
                .filter(|direction| bugs.contains(&(position + *direction)))
                .count();
            if gets_bug(bugs.contains(&position), adjacent_count) {
                new_state.push(position);
            }
        }
    }
    new_state
}

fn part1(bugs: &Bugs) -> usize {
    let mut bugs: Bugs = bugs.iter().copied().collect();
    let mut previous = HashSet::new();
    while previous.insert(bugs.clone()) {
        bugs = next_minute(&bugs);
    }
    let mut biodiversity = 0;
    for y in 0..5 {
        for x in 0..5 {
            if bugs.contains(&Bug::new(x, y)) {
                biodiversity += 1 << (y * 5 + x);
            }
        }
    }
    biodiversity
}

static CENTER: &'static Bug = &Bug::new(2, 2);
static MIDDLE_TOP: &'static Bug = &Bug::new(2, 1);
static MIDDLE_LEFT: &'static Bug = &Bug::new(1, 2);
static MIDDLE_RIGHT: &'static Bug = &Bug::new(3, 2);
static MIDDLE_BOTTOM: &'static Bug = &Bug::new(2, 3);

fn next_layered_minute(layers: &LayeredBugs) -> LayeredBugs {
    let mut new_state = LayeredBugs::new();
    for layer in layers.keys().min().unwrap() - 1..layers.keys().max().unwrap() + 2 {
        let mut layer_bugs = Bugs::new();
        for y in 0..5 {
            for x in 0..5 {
                let position = Bug::new(x, y);
                if position == *CENTER {
                    continue;
                }
                let mut adjacent_count = DIRECTIONS
                    .iter()
                    .filter(|direction| {
                        layers
                            .get(&layer)
                            .unwrap_or(&Bugs::new())
                            .contains(&(position + *direction))
                    })
                    .count();
                if let Some(lower_layer) = layers.get(&(layer - 1)) {
                    if y == 0 && lower_layer.contains(MIDDLE_TOP) {
                        adjacent_count += 1;
                    } else if y == 4 && lower_layer.contains(MIDDLE_BOTTOM) {
                        adjacent_count += 1;
                    }

                    if x == 0 && lower_layer.contains(MIDDLE_LEFT) {
                        adjacent_count += 1;
                    } else if x == 4 && lower_layer.contains(MIDDLE_RIGHT) {
                        adjacent_count += 1;
                    }
                }
                if let Some(upper_layer) = layers.get(&(layer + 1)) {
                    if position == *MIDDLE_TOP {
                        adjacent_count += (0..5)
                            .filter(|x| upper_layer.contains(&Bug::new(*x, 0)))
                            .count();
                    } else if position == *MIDDLE_LEFT {
                        adjacent_count += (0..5)
                            .filter(|y| upper_layer.contains(&Bug::new(0, *y)))
                            .count();
                    } else if position == *MIDDLE_RIGHT {
                        adjacent_count += (0..5)
                            .filter(|y| upper_layer.contains(&Bug::new(4, *y)))
                            .count();
                    } else if position == *MIDDLE_BOTTOM {
                        adjacent_count += (0..5)
                            .filter(|x| upper_layer.contains(&Bug::new(*x, 4)))
                            .count();
                    }
                }
                if gets_bug(
                    layers
                        .get(&layer)
                        .unwrap_or(&Bugs::new())
                        .contains(&(position)),
                    adjacent_count,
                ) {
                    layer_bugs.push(position);
                }
            }
        }
        new_state.insert(layer, layer_bugs);
    }
    new_state
}

fn part2(bugs: &Bugs) -> usize {
    let mut layers = LayeredBugs::new();
    layers.insert(0, bugs.iter().copied().collect());
    for _ in 0..200 {
        layers = next_layered_minute(&layers);
    }
    layers.values().fold(0, |acc, layer| acc + layer.len())
}

fn solve(bugs: &Bugs) -> (usize, usize) {
    (part1(bugs), part2(bugs))
}

fn get_input(file_path: &String) -> Bugs {
    let mut bugs = Bugs::new();
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                bugs.push(Bug::new(x as i32, y as i32));
            }
        }
    }
    bugs
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

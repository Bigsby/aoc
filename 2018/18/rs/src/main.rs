use num::complex::Complex;
use std::collections::HashMap;

#[derive(Debug, PartialEq, Copy, Clone)]
enum State {
    Open,
    Tree,
    Lumberyard,
}

impl State {
    fn parse(c: char) -> State {
        match c {
            '.' => State::Open,
            '|' => State::Tree,
            '#' => State::Lumberyard,
            _ => {
                panic!("Unrecognized state '{}'", c)
            }
        }
    }
}
type Position = Complex<i32>;
type Grid = HashMap<Position, State>;
static NEIGHBOR_DIRECTIONS: &'static [Position] = &[
    Position::new(-1, -1),
    Position::new(0, -1),
    Position::new(1, -1),
    Position::new(-1, 0),
    Position::new(1, 0),
    Position::new(-1, 1),
    Position::new(0, 1),
    Position::new(1, 1),
];

fn get_count_around(position: Position, grid: &Grid, state: &State) -> usize {
    NEIGHBOR_DIRECTIONS
        .into_iter()
        .filter(|direction| {
            let neighbor = position + **direction;
            grid.contains_key(&neighbor) && grid.get(&neighbor).unwrap() == state
        })
        .count()
}

fn get_next_minute(grid: &Grid) -> Grid {
    let mut new_state = Grid::new();
    for (position, state) in grid {
        new_state.insert(
            *position,
            match state {
                State::Open => {
                    if get_count_around(*position, grid, &State::Tree) > 2 {
                        State::Tree
                    } else {
                        State::Open
                    }
                }
                State::Tree => {
                    if get_count_around(*position, grid, &State::Lumberyard) > 2 {
                        State::Lumberyard
                    } else {
                        State::Tree
                    }
                }
                State::Lumberyard => {
                    if get_count_around(*position, grid, &State::Lumberyard) > 0
                        && get_count_around(*position, grid, &State::Tree) > 0
                    {
                        State::Lumberyard
                    } else {
                        State::Open
                    }
                }
            },
        );
    }
    new_state
}

fn get_resource_value(grid: &Grid) -> usize {
    grid.values().filter(|state| **state == State::Tree).count()
        * grid
            .values()
            .filter(|state| **state == State::Lumberyard)
            .count()
}

fn do_grids_match(a: &Grid, b: &Grid) -> bool {
    for pair in a {
        if b.get(pair.0).unwrap() != pair.1 {
            return false;
        }
    }
    true
}

fn find_repeat(previous: &Vec<Grid>, current: &Grid) -> Option<usize> {
    for index in 0..previous.len() {
        if do_grids_match(&previous[index], current) {
            return Some(index);
        }
    }
    None
}

fn solve(grid: &Grid) -> (usize, usize) {
    let mut grid: Grid = grid.into_iter().map(|(k, v)| (*k, *v)).collect();
    let mut previous_values = Vec::new();
    previous_values.push(grid.iter().map(|(k, v)| (*k, *v)).collect());
    let total = 1_000_000_000;
    let mut minute = 0;
    let mut part1_result = 0;
    let mut repeat_found = false;
    while minute < total {
        if minute == 10 {
            part1_result = get_resource_value(&grid);
        }
        minute += 1;
        grid = get_next_minute(&grid);
        let grid_values = grid.iter().map(|(k, v)| (*k, *v)).collect();
        if !repeat_found {
            if let Some(previous) = find_repeat(&previous_values, &grid_values) {
                repeat_found = true;
                let period = minute - previous;
                minute += ((total - minute) / period) * period;
            }
        }
        previous_values.push(grid_values);
    }
    (part1_result, get_resource_value(&grid))
}

fn get_input(file_path: &String) -> Grid {
    let mut grid = Grid::new();
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            grid.insert(Position::new(x as i32, y as i32), State::parse(c));
        }
    }
    grid
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

use num::Complex;
use std::collections::HashMap;

type Position = Complex<i32>;
type Grid = HashMap<Position, bool>;

static NEIGHBOR_DIRECTIONS: &'static [Position] = &[
    Position::new(-1, -1),
    Position::new(0, -1),
    Position::new(1, -1),
    Position::new(-1, 0),
    Position::new(1, 0),
    Position::new(-1, -1),
    Position::new(0, -1),
    Position::new(1, -1),
];

fn get_neighbors(position: &Position) -> Vec<Position> {
    NEIGHBOR_DIRECTIONS
        .into_iter()
        .map(|direction| position + direction)
        .collect()
}

fn get_next_state(grid: &Grid, always_on: &Vec<Position>) -> Grid {
    let mut new_state = Grid::new();
    for position in grid.keys() {
        let neighbors_active_count = get_neighbors(position)
            .into_iter()
            .filter(|neighbor| grid.contains_key(neighbor) && *grid.get(neighbor).unwrap())
            .count();
        new_state.insert(
            *position,
            if *grid.get(position).unwrap() {
                neighbors_active_count == 2 || neighbors_active_count == 3
            } else {
                neighbors_active_count == 3
            },
        );
    }
    for position in always_on {
        *new_state.get_mut(position).unwrap() = true;
    }
    new_state
}

fn run_steps(grid: &Grid, always_on: &Vec<Position>) -> usize {
    let mut grid = grid.clone();
    for position in always_on {
        *grid.get_mut(position).unwrap() = true;
    }
    for _ in 0..100 {
        grid = get_next_state(&grid, always_on);
    }
    grid.values().filter(|v| **v).count()
}

fn solve(grid: &Grid) -> (usize, usize) {
    let side = grid.keys().map(|p| p.re).max().unwrap();
    (
        run_steps(grid, &vec![]),
        run_steps(
            grid,
            &vec![
                Position::new(0, 0),
                Position::new(0, side),
                Position::new(side, 0),
                Position::new(side, side),
            ],
        ),
    )
}

fn get_input(file_path: &String) -> Grid {
    let mut grid = Grid::new();
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            grid.insert(Position::new(x as i32, y as i32), c == '#');
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

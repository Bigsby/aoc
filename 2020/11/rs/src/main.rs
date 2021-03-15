use num::complex::Complex;
use std::collections::HashMap;
use std::mem::{discriminant, Discriminant};

type Position = Complex<i32>;
type Grid = HashMap<Position, State>;
type NeighborFinder = fn(&Grid, &Position, &Position) -> Position;

pub enum State {
    Occupied,
    Empty,
    Floor,
}

impl State {
    fn parse(c: char) -> State {
        match c {
            '#' => State::Occupied,
            'L' => State::Empty,
            '.' => State::Floor,
            _ => panic!("Unrecognized state '{}'", c),
        }
    }

    fn clone(&self) -> State {
        match self {
            State::Empty => State::Empty,
            State::Floor => State::Floor,
            State::Occupied => State::Occupied,
        }
    }

    fn discriminant(&self) -> Discriminant<State> {
        discriminant(self)
    }
}

pub struct SeatProcessor {
    grid: Grid,
    neighbor_finder: NeighborFinder,
    neighbor_directions: Vec<Position>,
    tolerance: u32,
}

impl SeatProcessor {
    pub fn new(grid: &Grid, tolerance: u32, neighbor_finder: NeighborFinder) -> SeatProcessor {
        SeatProcessor {
            grid: grid
                .iter()
                .map(|(position, state)| (*position, state.clone()))
                .collect(),
            tolerance,
            neighbor_finder,
            neighbor_directions: vec![
                Complex::new(-1, -1),
                Complex::new(0, -1),
                Complex::new(1, -1),
                Complex::new(-1, 0),
                Complex::new(1, 0),
                Complex::new(-1, 1),
                Complex::new(0, 1),
                Complex::new(1, 1),
            ],
        }
    }

    fn get_occupied_count(&self, position: &Position) -> u32 {
        let mut total = 0;
        for direction in &self.neighbor_directions {
            let neighbor = (self.neighbor_finder)(&self.grid, position, &direction);
            if let Some(State::Occupied) = self.grid.get(&neighbor) {
                total += 1;
            }
        }
        total
    }

    fn get_position_new_state(&self, position: &Position) -> (bool, State) {
        let current_state = self.grid.get(position).unwrap();
        if State::Floor.discriminant() == current_state.discriminant() {
            return (false, State::Floor);
        }
        let occupied_count = self.get_occupied_count(position);
        if State::Empty.discriminant() == current_state.discriminant() && occupied_count == 0 {
            return (true, State::Occupied);
        }
        if State::Occupied.discriminant() == current_state.discriminant()
            && occupied_count > self.tolerance
        {
            return (true, State::Empty);
        }
        (false, current_state.clone())
    }

    fn get_next_state(&mut self) -> bool {
        let mut new_state: Grid = self
            .grid
            .iter()
            .clone()
            .map(|(key, value)| (*key, value.clone()))
            .collect();
        let mut any_change = false;
        for position in self.grid.keys() {
            let (changed, new_position_state) = self.get_position_new_state(position);
            any_change |= changed;
            new_state
                .entry(*position)
                .and_modify(|value| *value = new_position_state);
        }
        self.grid = new_state;
        any_change
    }

    pub fn run_grid(&mut self) -> usize {
        while self.get_next_state() {}
        self.grid
            .values()
            .filter(|value| State::Occupied.discriminant() == value.discriminant())
            .count()
    }
}

fn get_directional_neighbor(grid: &Grid, position: &Position, direction: &Position) -> Position {
    let mut position = position + direction;
    while let Some(State::Floor) = grid.get(&position) {
        position += direction;
    }
    position
}

fn solve(grid: &Grid) -> (usize, usize) {
    (
        SeatProcessor::new(grid, 3, |_, position, direction| position + direction).run_grid(),
        SeatProcessor::new(grid, 4, get_directional_neighbor).run_grid(),
    )
}

fn get_input(file_path: &String) -> Grid {
    let mut grid = Grid::new();
    std::fs::read_to_string(file_path).expect("Error reading input file!");
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            grid.insert(Complex::new(x as i32, y as i32), State::parse(c));
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

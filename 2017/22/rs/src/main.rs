use num::Complex;
use std::collections::HashMap;

type Lattice = Complex<i32>;
type InfectionStatus = HashMap<Lattice, bool>;

fn part1(state: &InfectionStatus) -> usize {
    let mut state = state.clone();
    let mut infection_count = 0;
    let mut current_node = Lattice::new(
        state.keys().map(|l| l.re).max().unwrap() / 2,
        state.keys().map(|l| l.im).min().unwrap() / 2,
    );
    let mut direction = Lattice::new(0, 1);
    const LEFT: Lattice = Lattice::new(0, 1);
    const RIGHT: Lattice = Lattice::new(0, -1);
    for _ in 0..10_000 {
        let node_state = *state.entry(current_node).or_insert(false);
        direction *= if node_state { RIGHT } else { LEFT };
        *state.get_mut(&current_node).unwrap() = !node_state;
        current_node += direction;
        if !node_state {
            infection_count += 1;
        }
    }
    infection_count
}

const CLEAN: usize = 0;
const WEAKENED: usize = 1;
const INFECTED: usize = 2;
const FLAGGED: usize = 3;
static STATE_DIRECTIONS: &'static [Lattice] = &[
    Lattice::new(0, 1),
    Lattice::new(1, 0),
    Lattice::new(0, -1),
    Lattice::new(-1, 0),
];
static STATE_TRANSITIONS: &'static [usize] = &[WEAKENED, INFECTED, FLAGGED, CLEAN];

fn part2(state: &InfectionStatus) -> usize {
    let mut quad_state: HashMap<Lattice, usize> = state
        .into_iter()
        .map(|(lattice, state)| (*lattice, if *state { INFECTED } else { CLEAN }))
        .collect();
    let mut infection_count = 0;
    let mut current_node = Lattice::new(
        state.keys().map(|l| l.re).max().unwrap() / 2,
        state.keys().map(|l| l.im).min().unwrap() / 2,
    );
    let mut direction = Lattice::new(0, 1);
    for _ in 0..10_000_000 {
        let node_state = *quad_state.entry(current_node).or_insert(CLEAN);
        let new_state = STATE_TRANSITIONS[node_state];
        direction *= STATE_DIRECTIONS[node_state];
        *quad_state.get_mut(&current_node).unwrap() = new_state;
        current_node += direction;
        if new_state == INFECTED {
            infection_count += 1;
        }
    }
    infection_count
}

fn solve(state: &InfectionStatus) -> (usize, usize) {
    (part1(state), part2(state))
}

fn get_input(file_path: &String) -> InfectionStatus {
    let mut infection_status = InfectionStatus::new();
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            infection_status.insert(Lattice::new(x as i32, -(y as i32)), c == '#');
        }
    }
    infection_status
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

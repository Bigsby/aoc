use core::cell::RefCell;
use num::Complex;
use regex::Regex;
use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};

type Lattice = Complex<i32>;
const GEOLOGIC_X_CONSTANT: i32 = 16807;
const GEOLOGIC_Y_CONSTANT: i32 = 48271;
const EROSION_CONSTANT: i32 = 20183;

struct RiskCalculator {
    calculated: RefCell<HashMap<Lattice, i32>>,
    depth: i32,
    target: Lattice,
}

impl RiskCalculator {
    fn new(depth: i32, target: Lattice) -> RiskCalculator {
        RiskCalculator {
            calculated: RefCell::new(HashMap::new()),
            depth,
            target,
        }
    }

    fn get_geologic_index(&mut self, lattice: &Lattice) -> i32 {
        if *lattice == Lattice::new(0, 0) || lattice == &self.target {
            return 0;
        }
        let (x, y) = (lattice.re, lattice.im);
        if x == 0 {
            return y * GEOLOGIC_Y_CONSTANT;
        } else if y == 0 {
            return x * GEOLOGIC_X_CONSTANT;
        }
        self.get_erosion_level(&Lattice::new(x - 1, y))
            * self.get_erosion_level(&Lattice::new(x, y - 1))
    }

    fn get_erosion_level(&mut self, lattice: &Lattice) -> i32 {
        if !self.calculated.borrow().contains_key(lattice) {
            let new_value = (self.get_geologic_index(lattice) + self.depth) % EROSION_CONSTANT;
            self.calculated.borrow_mut().insert(*lattice, new_value);
        }
        *self.calculated.borrow().get(lattice).unwrap()
    }

    pub fn get_risk(&mut self, lattice: &Lattice) -> i32 {
        self.get_erosion_level(lattice) % 3
    }
}

fn part1(data: &(i32, i32, i32)) -> i32 {
    let (depth, target_x, target_y) = data;
    let target = Lattice::new(*target_x, *target_y);
    let mut risk_calculator = RiskCalculator::new(*depth, target);
    let mut total = 0;
    for x in 0..target_x + 1 {
        for y in 0..target_y + 1 {
            total += risk_calculator.get_risk(&Lattice::new(x, y));
        }
    }
    total
}

static DIRECTIONS: &'static [Lattice] = &[
    Lattice::new(1, 0),
    Lattice::new(0, 1),
    Lattice::new(-1, 0),
    Lattice::new(0, -1),
];

#[derive(Eq, PartialEq, Debug)]
struct Node {
    duration: i32,
    x: i32,
    y: i32,
    risk: i32,
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        other
            .duration
            .cmp(&self.duration)
            .then_with(|| other.x.cmp(&self.x))
            .then_with(|| other.y.cmp(&self.y))
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn part2(data: &(i32, i32, i32)) -> i32 {
    let (depth, x, y) = data;
    let target = Lattice::new(*x, *y);
    let mut risk_calculator = RiskCalculator::new(*depth, target);
    let final_: (i32, i32, i32) = (*x, *y, 1);
    let mut queue = BinaryHeap::new();
    queue.push(Node {
        duration: 0,
        x: 0,
        y: 0,
        risk: 1,
    }); // 1 = torch, 0 neither, 2 climbing
    let mut best_times: HashMap<(i32, i32, i32), i32> = HashMap::new();
    while let Some(Node {
        duration,
        x,
        y,
        risk,
    }) = queue.pop()
    {
        let lattice = Lattice::new(x, y);
        let state = (x, y, risk);
        if let Some(previous_best) = best_times.get(&state) {
            if *previous_best <= duration {
                continue;
            }
        }
        if state == final_ {
            return duration;
        }
        best_times.insert(state, duration);
        for tool in 0..3 {
            if tool != risk && tool != risk_calculator.get_risk(&lattice) {
                queue.push(Node {
                    duration: duration + 7,
                    x,
                    y,
                    risk: tool,
                });
            }
        }
        for direction in DIRECTIONS {
            let new_lattice = lattice + direction;
            if new_lattice.re >= 0
                && new_lattice.im >= 0
                && risk_calculator.get_risk(&new_lattice) != risk
            {
                queue.push(Node {
                    duration: duration + 1,
                    x: new_lattice.re,
                    y: new_lattice.im,
                    risk,
                });
            }
        }
    }
    panic!("Path not found");
}

fn solve(data: &(i32, i32, i32)) -> (i32, i32) {
    (part1(data), part2(data))
}

fn get_input(file_path: &String) -> (i32, i32, i32) {
    let numbers = Regex::new(r"\d+")
        .unwrap()
        .captures_iter(&std::fs::read_to_string(file_path).expect("Error reading input file!"))
        .map(|cap| cap.get(0).unwrap().as_str().parse().unwrap())
        .collect::<Vec<i32>>();
    (numbers[0], numbers[1], numbers[2])
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

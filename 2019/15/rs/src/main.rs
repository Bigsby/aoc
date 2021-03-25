use num::complex::Complex;
use std::cell::RefCell;
use std::collections::{HashMap, HashSet, VecDeque};

type Position = Complex<i32>;
static DIRECTIONS: &'static [(i64, Position); 4] = &[
    (1, Position::new(0, -1)),
    (2, Position::new(0, 1)),
    (3, Position::new(-1, 0)),
    (4, Position::new(1, 0)),
];

#[derive(Clone)]
pub struct IntCodeComputer {
    memory: RefCell<HashMap<i64, i64>>,
    input: RefCell<VecDeque<i64>>,
    output: RefCell<VecDeque<i64>>,
    pointer: i64,
    base: i64,
    pub running: bool,
    pub outputing: bool,
    pub polling: bool,
}

impl IntCodeComputer {
    pub fn new(memory: &Vec<i64>, input: Vec<i64>) -> IntCodeComputer {
        IntCodeComputer {
            memory: RefCell::new(
                memory
                    .clone()
                    .into_iter()
                    .enumerate()
                    .map(|(index, value)| (index as i64, value))
                    .collect(),
            ),
            input: RefCell::new(VecDeque::from(input)),
            output: RefCell::new(VecDeque::new()),
            pointer: 0,
            base: 0,
            running: true,
            outputing: false,
            polling: false,
        }
    }

    pub fn run(&mut self) -> i64 {
        while self.tick() {}
        self.output.borrow_mut().pop_front().unwrap()
    }

    pub fn get_output(&mut self) -> i64 {
        self.outputing = false;
        self.output.borrow_mut().pop_front().unwrap()
    }

    fn add_input(&mut self, value: i64) {
        self.input.borrow_mut().push_back(value);
    }

    fn get_memory_value(&self, location: i64) -> i64 {
        if let Some(value) = self.memory.borrow().get(&location) {
            *value
        } else {
            0
        }
    }

    fn get_parameter(&self, offset: i64, mode: i64) -> i64 {
        let value = self.get_memory_value(self.pointer + offset);
        match mode {
            0 => self.get_memory_value(value),             // POSITION
            1 => value,                                    // IMMEDIATE
            2 => self.get_memory_value(self.base + value), // RELATIVE
            _ => {
                panic!("Unrecognized parameter mode '{}'", mode);
            }
        }
    }

    fn get_address(&self, offset: i64, mode: i64) -> i64 {
        let value = self.get_memory_value(self.pointer + offset);
        match mode {
            0 => value,             // POSITION
            2 => self.base + value, // RELATIVE
            _ => {
                panic!("Unrecognized address mode '{}'", mode);
            }
        }
    }

    fn set_memory(&mut self, offset: i64, mode: i64, value: i64) {
        let address = self.get_address(offset, mode);
        *self.memory.borrow_mut().entry(address).or_insert(0) = value;
    }

    fn tick(&mut self) -> bool {
        if !self.running {
            return false;
        }
        let instruction = *self.memory.borrow().get(&self.pointer).unwrap();
        let (opcode, p1_mode, p2_mode, p3_mode) = (
            instruction % 100,
            (instruction / 100) % 10,
            (instruction / 1000) % 10,
            (instruction / 10000) % 10,
        );
        match opcode {
            1 => {
                // ADD
                self.set_memory(
                    3,
                    p3_mode,
                    self.get_parameter(1, p1_mode) + self.get_parameter(2, p2_mode),
                );
                self.pointer += 4;
            }
            2 => {
                // MUL
                self.set_memory(
                    3,
                    p3_mode,
                    self.get_parameter(1, p1_mode) * self.get_parameter(2, p2_mode),
                );
                self.pointer += 4;
            }
            3 => {
                // INPUT
                let input = self.input.borrow_mut().pop_front();
                if let Some(value) = input {
                    self.polling = false;
                    self.set_memory(1, p1_mode, value);
                    self.pointer += 2;
                } else {
                    self.polling = true;
                }
            }
            4 => {
                // OUTPUT
                self.outputing = true;
                self.output
                    .borrow_mut()
                    .push_back(self.get_parameter(1, p1_mode));
                self.pointer += 2;
            }
            5 => {
                // JMP_TRUE
                if self.get_parameter(1, p1_mode) != 0 {
                    self.pointer = self.get_parameter(2, p2_mode);
                } else {
                    self.pointer += 3;
                }
            }
            6 => {
                // JMP_FALSE
                if self.get_parameter(1, p1_mode) == 0 {
                    self.pointer = self.get_parameter(2, p2_mode);
                } else {
                    self.pointer += 3;
                }
            }
            7 => {
                // LESS_THAN
                self.set_memory(
                    3,
                    p3_mode,
                    if self.get_parameter(1, p1_mode) < self.get_parameter(2, p2_mode) {
                        1
                    } else {
                        0
                    },
                );
                self.pointer += 4;
            }
            8 => {
                // EQUALS
                self.set_memory(
                    3,
                    p3_mode,
                    if self.get_parameter(1, p1_mode) == self.get_parameter(2, p2_mode) {
                        1
                    } else {
                        0
                    },
                );
                self.pointer += 4;
            }
            9 => {
                // SET_BASE
                self.base += self.get_parameter(1, p1_mode);
                self.pointer += 2;
            }
            99 => {
                // HALT
                self.running = false;
            }
            _ => panic!("Unknown instruction {} {}", self.pointer, opcode),
        }
        self.running
    }
}

fn _draw_area(oxygen: &Vec<Position>, walls: &Vec<Position>, open_spaces: &Vec<Position>) {
    let mut all_posiitons = oxygen.clone();
    all_posiitons.extend(walls);
    let min_x = all_posiitons.iter().map(|p| p.re).min().unwrap();
    let max_x = all_posiitons.iter().map(|p| p.re).max().unwrap();
    let min_y = all_posiitons.iter().map(|p| p.im).min().unwrap();
    let max_y = all_posiitons.iter().map(|p| p.im).max().unwrap();
    for y in (min_y - 1..max_y).rev() {
        for x in min_x..max_x + 1 {
            let mut c = ' ';
            let position = &Position::new(x, y);
            if walls.contains(position) {
                c = '#';
            } else if open_spaces.contains(position) {
                c = '.';
            } else if oxygen.contains(position) {
                c = 'o';
            }
            print!("{}", c);
        }
        println!();
    }
    println!();
}

fn _pause() {
    let mut input: String = String::new();
    std::io::stdin()
        .read_line(&mut input)
        .expect("error inputing");
}

fn run_until_oxygen_system(memory: &Vec<i64>) -> (usize, Position, Vec<Position>) {
    let start_position = Position::new(0, 0);
    let mut open_spaces = Vec::new();
    let mut oxygen_system_position = Position::new(0, 0);
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();
    queue.push_back((
        start_position,
        vec![start_position],
        IntCodeComputer::new(memory, vec![]),
    ));
    let mut steps_to_oxygen_system = 0;
    while let Some((position, path, droid)) = queue.pop_front() {
        for (command, direction) in DIRECTIONS {
            let new_position = position + direction;
            if visited.insert(new_position) {
                let mut new_droid = droid.clone();
                new_droid.add_input(*command);
                while !new_droid.outputing {
                    new_droid.tick();
                }
                let status = new_droid.get_output();
                if status == 2 {
                    // Oxygen System
                    if steps_to_oxygen_system == 0 {
                        steps_to_oxygen_system = path.len();
                    }
                    oxygen_system_position = new_position;
                } else if status == 1 {
                    // Open Space
                    open_spaces.push(new_position);
                    while !new_droid.polling {
                        new_droid.tick();
                    }
                    let mut new_path = path.clone();
                    new_path.push(new_position);
                    queue.push_back((new_position, new_path, new_droid));
                }
            }
        }
    }
    (steps_to_oxygen_system, oxygen_system_position, open_spaces)
}

fn solve(memory: &Vec<i64>) -> (usize, usize) {
    let (steps_to_oxygen_system, oxygen_system_position, open_spaces) =
        run_until_oxygen_system(memory);
    let mut filled = vec![oxygen_system_position];
    let mut open_spaces = open_spaces.clone();
    let mut minutes = 0;
    while !open_spaces.is_empty() {
        minutes += 1;
        for oxygen in &filled.clone() {
            for (_, direction) in DIRECTIONS {
                let position = oxygen + direction;
                if let Some(index) = open_spaces.iter().position(|p| *p == position) {
                    filled.push(position);
                    open_spaces.remove(index);
                }
            }
        }
    }
    (steps_to_oxygen_system, minutes)
}

fn get_input(file_path: &String) -> Vec<i64> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split(',')
        .map(|i| i.trim().parse().unwrap())
        .collect()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        panic!("Please, add input file path as parameter");
    }
    let now = std::time::Instant::now();
    let (part1_result, part2_result) = solve(&get_input(&args[1]));
    println!("P1: {}", part1_result);
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:.7}", now.elapsed().as_secs_f32());
}

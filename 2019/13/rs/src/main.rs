use num::complex::Complex;
use std::cell::RefCell;
use std::collections::HashMap;
use std::collections::VecDeque;

enum Tile {
    Empty,
    Wall,
    Block,
    Paddle,
    Ball,
}

impl Tile {
    fn from_i64(value: i64) -> Result<Tile, ()> {
        match value {
            0 => Ok(Tile::Empty),
            1 => Ok(Tile::Wall),
            2 => Ok(Tile::Block),
            3 => Ok(Tile::Paddle),
            4 => Ok(Tile::Ball),
            _ => Err(()),
        }
    }

    fn to_i64(&self) -> i64 {
        match self {
            Tile::Empty => 0,
            Tile::Wall => 1,
            Tile::Block => 2,
            Tile::Paddle => 3,
            Tile::Ball => 4,
        }
    }
}

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

fn _print_screen(screen: &HashMap<Complex<i64>, Tile>) {
    let tile_chars: HashMap<i64, char> = vec![(0, '.'), (1, 'W'), (2, 'B'), (3, 'P'), (4, 'X')]
        .into_iter()
        .collect();
    let max_x = screen.keys().map(|p| p.re).max().unwrap();
    let min_x = screen.keys().map(|p| p.re).min().unwrap();
    let max_y = screen.keys().map(|p| p.im).max().unwrap();
    let min_y = screen.keys().map(|p| p.im).min().unwrap();
    for y in min_y..max_y + 1 {
        for x in min_x..max_x + 1 {
            let position = Complex::new(x, y);
            let mut c = ' ';
            if let Some(tile) = screen.get(&position) {
                if let Some(tile_c) = tile_chars.get(&tile.to_i64()) {
                    c = *tile_c;
                }
            }
            print!("{}", c);
        }
        println!();
    }
    println!();
}

fn run_game(memory: &Vec<i64>) -> (usize, i64) {
    let mut cabinet = IntCodeComputer::new(memory, vec![]);
    let mut screen = HashMap::new();
    let mut current_ouput = Vec::new();
    let mut ball = 0;
    let mut paddle = 0;
    let mut score = 0;
    while cabinet.running {
        cabinet.tick();
        if cabinet.polling {
            let mut joystick = 0;
            if ball > paddle {
                joystick = 1;
            } else if ball < paddle {
                joystick = -1;
            }
            cabinet.add_input(joystick);
        }
        if cabinet.outputing {
            current_ouput.push(cabinet.get_output());
            if current_ouput.len() == 3 {
                let value = current_ouput.pop().unwrap();
                let y = current_ouput.pop().unwrap();
                let x = current_ouput.pop().unwrap();
                if x == -1 {
                    score = value;
                } else {
                    let tile = Tile::from_i64(value);
                    match Tile::from_i64(value) {
                        Ok(Tile::Ball) => ball = x,
                        Ok(Tile::Paddle) => paddle = x,
                        _ => {}
                    }
                    *screen.entry(Complex::new(x, y)).or_insert(Tile::Empty) = tile.unwrap();
                }
            }
        }
    }
    (
        screen
            .values()
            .filter(|t| t.to_i64() == Tile::Block.to_i64())
            .count(),
        score,
    )
}

fn solve(memory: &Vec<i64>) -> (usize, i64) {
    let part1_result = run_game(memory).0;
    let mut memory = memory.clone();
    memory[0] = 2;
    (part1_result, run_game(&memory).1)
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

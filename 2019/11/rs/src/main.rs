use num::complex::Complex;
use std::cell::RefCell;
use std::collections::HashMap;
use std::collections::VecDeque;

const CHARACTER_WIDTH: u32 = 5;

struct LetterMap {
    letters: HashMap<u32, char>,
}

impl LetterMap {
    fn new() -> LetterMap {
        LetterMap {
            letters: vec![
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b11110 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'A',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b11100 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b11100 << CHARACTER_WIDTH * 5),
                    'B',
                ),
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'C',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b11100 << CHARACTER_WIDTH * 5),
                    'D',
                ),
                (
                      (0b11110 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b11100 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b11110 << CHARACTER_WIDTH * 5),
                    'E',
                ),
                (
                      (0b11110 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b11100 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b10000 << CHARACTER_WIDTH * 5),
                    'F',
                ),
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b10110 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01110 << CHARACTER_WIDTH * 5),
                    'G',
                ),
                (
                      (0b10010 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b11110 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'H',
                ),
                (
                      (0b01110 << CHARACTER_WIDTH * 0)
                    + (0b00100 << CHARACTER_WIDTH * 1)
                    + (0b00100 << CHARACTER_WIDTH * 2)
                    + (0b00100 << CHARACTER_WIDTH * 3)
                    + (0b00100 << CHARACTER_WIDTH * 4)
                    + (0b01110 << CHARACTER_WIDTH * 5),
                    'I',
                ),
                (
                      (0b00110 << CHARACTER_WIDTH * 0)
                    + (0b00010 << CHARACTER_WIDTH * 1)
                    + (0b00010 << CHARACTER_WIDTH * 2)
                    + (0b00010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'J',
                ),
                (
                      (0b10010 << CHARACTER_WIDTH * 0)
                    + (0b10100 << CHARACTER_WIDTH * 1)
                    + (0b11000 << CHARACTER_WIDTH * 2)
                    + (0b10100 << CHARACTER_WIDTH * 3)
                    + (0b10100 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'K',
                ),
                (
                      (0b10000 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b11110 << CHARACTER_WIDTH * 5),
                    'L',
                ),
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'O',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b11100 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b10000 << CHARACTER_WIDTH * 5),
                    'P',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b11100 << CHARACTER_WIDTH * 3)
                    + (0b10100 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'R',
                ),
                (
                      (0b01110 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b01100 << CHARACTER_WIDTH * 3)
                    + (0b00010 << CHARACTER_WIDTH * 4)
                    + (0b11100 << CHARACTER_WIDTH * 5),
                    'S',
                ),
                (
                      (0b10010 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'U',
                ),
                (
                      (0b10001 << CHARACTER_WIDTH * 0)
                    + (0b10001 << CHARACTER_WIDTH * 1)
                    + (0b01010 << CHARACTER_WIDTH * 2)
                    + (0b00100 << CHARACTER_WIDTH * 3)
                    + (0b00100 << CHARACTER_WIDTH * 4)
                    + (0b00100 << CHARACTER_WIDTH * 5),
                    'Y',
                ),
                (
                      (0b11110 << CHARACTER_WIDTH * 0)
                    + (0b00010 << CHARACTER_WIDTH * 1)
                    + (0b00100 << CHARACTER_WIDTH * 2)
                    + (0b01000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b11110 << CHARACTER_WIDTH * 5),
                    'Z',
                ),
            ]
            .into_iter()
            .collect::<HashMap<u32, char>>(),
        }
    }

    fn get(&self, code: u32) -> char {
        *self.letters.get(&code).unwrap()
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

fn run_program(memory: &Vec<i64>, origin_value: i64) -> HashMap<Complex<i32>, i64> {
    let direction_changes: HashMap<i64, Complex<i32>> =
        vec![(0, Complex::new(0, 1)), (1, Complex::new(0, -1))]
            .into_iter()
            .collect();
    let mut robot = IntCodeComputer::new(memory, vec![]);
    let mut panels = HashMap::new();
    panels.insert(Complex::new(0, 0), origin_value);
    let mut position = Complex::new(0, 0);
    let mut heading = Complex::new(0, 1);
    let mut waiting_for_color = true;
    while robot.running {
        robot.tick();
        if robot.polling {
            robot.add_input(*panels.entry(position).or_insert(0));
        } else if robot.outputing {
            if waiting_for_color {
                waiting_for_color = false;
                panels.insert(position, robot.get_output());
            } else {
                waiting_for_color = true;
                heading *= direction_changes[&robot.get_output()];
                position += heading;
            }
        }
    }
    panels
}

fn get_dimensions(points: &Vec<Complex<i32>>) -> ((u32, u32), i32, i32, i32, i32) {
    let min_x = points.iter().map(|point| point.re).min().unwrap();
    let max_x = points.iter().map(|point| point.re).max().unwrap();
    let min_y = points.iter().map(|point| point.im).min().unwrap();
    let max_y = points.iter().map(|point| point.im).max().unwrap();
    let size = (
        i32::abs(max_x - min_x + 1) as u32,
        i32::abs(max_y - min_y + 1) as u32,
    );
    (size, min_x, max_x, min_y, max_y)
}

fn _print_points(points: &Vec<Complex<i32>>) {
    let (_, min_x, max_x, min_y, max_y) = get_dimensions(points);
    for y in min_y..max_y + 1 {
        for x in min_x..max_x + 1 {
            print!(
                "{}",
                if points.contains(&Complex::new(x, y)) {
                    "#"
                } else {
                    "."
                }
            );
        }
        println!("");
    }
    println!("");
}

fn get_character_in_screen(
    screen: &Vec<Complex<i32>>,
    index: u32,
    width: u32,
    height: u32,
    x_offset: i32,
    y_offset: i32,
    letter_map: &LetterMap,
) -> char {
    let mut screen_value = 0;
    for x in 0..width {
        for y in 0..height {
            if screen.contains(&Complex::new(
                (width * index + x) as i32 + x_offset,
                y as i32 + y_offset,
            )) {
                screen_value += u32::pow(2, width - 1 - x) << (y * width);
            }
        }
    }
    letter_map.get(screen_value)
}

fn part2(memory: &Vec<i64>) -> String {
    let panels = run_program(memory, 1);
    let panel_points: Vec<Complex<i32>> = panels
        .into_iter()
        .filter(|(_, value)| *value > 0)
        .map(|(position, _)| Complex::new(position.re, -position.im))
        .collect();
    let ((width, height), min_x, _, min_y, _) = get_dimensions(&panel_points);
    let letter_map = LetterMap::new();
    (0..(width / CHARACTER_WIDTH) + 1)
        .into_iter()
        .map(|index| {
            get_character_in_screen(
                &panel_points,
                index,
                CHARACTER_WIDTH,
                height,
                min_x,
                min_y,
                &letter_map,
            )
        })
        .collect::<String>()
}

fn solve(memory: &Vec<i64>) -> (usize, String) {
    (run_program(memory, 0).len(), part2(memory))
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

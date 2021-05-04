use num::complex::Complex;
use std::cell::RefCell;
use std::collections::{HashMap, VecDeque};

static DIRECTIONS: &'static [(u8, Complex<i32>)] = &[
    (b'v', Complex::new(0, 1)),
    (b'>', Complex::new(1, 0)),
    (b'^', Complex::new(0, -1)),
    (b'<', Complex::new(-1, 0)),
];
type Scafolds = Vec<Complex<i32>>;
type Robot = (Complex<i32>, Complex<i32>);
type Path = Vec<String>;

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
        self.output.borrow_mut().pop_back().unwrap()
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

fn _print_area(scafolds: &Scafolds, robot: &Robot) {
    let min_x = scafolds.iter().map(|p| p.re).min().unwrap();
    let max_x = scafolds.iter().map(|p| p.re).max().unwrap();
    let min_y = scafolds.iter().map(|p| p.im).min().unwrap();
    let max_y = scafolds.iter().map(|p| p.im).max().unwrap();
    println!("{} {} {} {}", min_x, max_x, min_y, max_y);
    println!("{:?}", robot);
    for y in min_y..max_y + 1 {
        for x in min_x..max_x + 1 {
            let position = Complex::new(x, y);
            let mut c = '.';
            if scafolds.contains(&position) {
                c = '#';
            }
            if position == robot.0 {
                c = 'R';
            }
            print!("{}", c);
        }
        println!();
    }
    println!();
}

fn get_scalfolds_and_robot(ascii_computper: &mut IntCodeComputer) -> (Scafolds, Robot) {
    let mut position = Complex::new(0, 0);
    let mut scafolds = Scafolds::new();
    let mut robot = (Complex::new(0, 0), Complex::new(0, 0));
    let directions: HashMap<u8, Complex<i32>> = DIRECTIONS.into_iter().map(|p| *p).collect();
    while ascii_computper.running {
        ascii_computper.tick();
        if ascii_computper.outputing {
            match ascii_computper.get_output() {
                35 => {
                    // '#'
                    scafolds.push(position);
                    position += 1;
                }
                46 => {
                    // '.'
                    position += 1;
                }
                10 => {
                    // line feed
                    position = Complex::new(0, position.im + 1);
                }
                code => {
                    robot = (position, *directions.get(&(code as u8)).unwrap());
                    position += 1;
                }
            }
        }
    }
    (scafolds, robot)
}

fn part1(scafolds: &Scafolds) -> i32 {
    let mut alignment = 0;
    for scafold in scafolds {
        if DIRECTIONS
            .iter()
            .all(|direction| scafolds.contains(&(scafold + direction.1)))
        {
            alignment += scafold.re * scafold.im;
        }
    }
    alignment
}

fn find_path(scafolds: &Scafolds, robot: &Robot) -> Path {
    let mut robot = *robot;
    const TURNS: [(Complex<i32>, &str); 2] =
        [(Complex::new(0, -1), "L"), (Complex::new(0, 1), "R")];
    let mut path = Path::new();
    let mut current_turn = "";
    let mut turn_found = true;
    while turn_found {
        let (position, direction) = robot;
        if !scafolds.contains(&(position + direction)) {
            turn_found = false;
            for (turn, code) in &TURNS {
                if scafolds.contains(&(position + direction * turn)) {
                    turn_found = true;
                    current_turn = *code;
                    robot = (position, direction * turn);
                }
            }
        } else {
            let mut current_length = 0;
            let mut position = position;
            while scafolds.contains(&(position + direction)) {
                position += direction;
                current_length += 1;
            }
            robot = (position, direction);
            path.push(String::from(current_turn));
            path.push(current_length.to_string());
        }
    }
    path
}

fn find_routines(path: &Path) -> Vec<String> {
    let mut stack: Vec<(Vec<String>, Vec<Vec<String>>, usize)> = vec![(vec![], vec![], 0)];
    let routine_ids = "ABC".chars().collect::<Vec<char>>();
    while let Some((main, programs, index)) = stack.pop() {
        if index >= path.len() {
            let mut result = vec![main.join(",")];
            result.append(&mut programs.iter().map(|program| program.join(",")).collect());
            return result;
        }
        if main.len() < 10 {
            for (id, program) in routine_ids.iter().zip(&programs) {
                if index + program.len() <= path.len()
                    && path[index..index + program.len()] == *program
                {
                    stack.push((
                        vec![main.clone(), vec![id.to_string()]].concat(),
                        programs.iter().map(|p| p.clone()).collect(),
                        index + program.len(),
                    ));
                }
            }
        }
        if programs.len() < 3 {
            for end in index + 1..path.len() {
                if path[index..end]
                    .iter()
                    .map(|segment| segment.len())
                    .sum::<usize>()
                    + end
                    - index
                    - 1
                    > 20
                {
                    break;
                }
                stack.push((
                    vec![main.clone(), vec![routine_ids[programs.len()].to_string()]].concat(),
                    vec![
                        programs.clone(),
                        vec![path[index..end].iter().map(|s| s.clone()).collect()],
                    ]
                    .concat(),
                    end,
                ));
            }
        }
    }
    panic!("Routines not found")
}

fn part2(memory: &Vec<i64>, scafolds: &Scafolds, robot: &Robot) -> i64 {
    let mut memory: Vec<i64> = memory.into_iter().map(|i| *i).collect();
    memory[0] = 2;
    let mut ascii_computer = IntCodeComputer::new(&memory, vec![]);
    let path = find_path(scafolds, robot);
    let routines = find_routines(&path);
    let routines_text = routines.join("\n");
    let inputs = format!("{}\nn\n", routines_text);
    for c in inputs.chars() {
        ascii_computer.add_input((c as u8) as i64);
    }
    ascii_computer.run()
}

fn solve(memory: &Vec<i64>) -> (i32, i64) {
    let mut ascii_computer = IntCodeComputer::new(memory, vec![]);
    let (scafolds, robot) = get_scalfolds_and_robot(&mut ascii_computer);
    return (part1(&scafolds), part2(memory, &scafolds, &robot));
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

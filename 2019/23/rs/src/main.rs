use std::cell::RefCell;
use std::collections::{HashMap, VecDeque};

#[derive(Clone)]
pub struct IntCodeComputer {
    memory: RefCell<HashMap<i64, i64>>,
    input: RefCell<VecDeque<i64>>,
    output: RefCell<VecDeque<i64>>,
    pointer: i64,
    base: i64,
    default_input: bool,
    default_value: i64,
    pub running: bool,
    pub outputing: bool,
    pub polling: bool,
}

impl IntCodeComputer {
    pub fn new(
        memory: &Vec<i64>,
        input: Vec<i64>,
        default_input: bool,
        default_value: i64,
    ) -> IntCodeComputer {
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
            default_input,
            default_value,
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

    fn output_count(&self) -> usize {
        self.output.borrow().len()
    }

    fn input_count(&self) -> usize {
        self.input.borrow().len()
    }

    fn clear_inputs(&mut self) {
        self.input.borrow_mut().clear();
        self.polling = false;
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
                } else if self.default_input {
                    self.polling = true;
                    self.set_memory(1, p1_mode, self.default_value);
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

fn _pause() {
    std::io::stdin().read_line(&mut String::new()).expect("");
}

fn part1(memory: &Vec<i64>) -> i64 {
    let mut network: Vec<IntCodeComputer> = (0..50)
        .map(|address| IntCodeComputer::new(memory, vec![address as i64], false, 0))
        .collect();
    loop {
        let mut inputs = Vec::new();
        for computer in network.iter_mut() {
            computer.tick();
            if computer.outputing {
                if computer.output_count() == 3 {
                    let address = computer.get_output();
                    let x = computer.get_output();
                    let y = computer.get_output();
                    if address == 255 {
                        return y;
                    }
                    inputs.push((address as usize, x, y));
                }
            } else if computer.polling && computer.input_count() == 0 {
                computer.add_input(-1);
            }
        }
        for (address, x, y) in inputs {
            network[address].add_input(x);
            network[address].add_input(y);
        }
    }
}

fn part2(memory: &Vec<i64>) -> i64 {
    let mut network: Vec<IntCodeComputer> = (0..50)
        .map(|address| IntCodeComputer::new(memory, vec![address], true, -1))
        .collect();
    let mut sent_ys: Vec<i64> = Vec::new();
    let mut nat_packet = (0, 0);
    loop {
        let mut inputs = Vec::new();
        for computer in network.iter_mut() {
            computer.tick();
            if computer.outputing {
                if computer.output_count() == 3 {
                    let address = computer.get_output();
                    let x = computer.get_output();
                    let y = computer.get_output();
                    if address == 255 {
                        nat_packet = (x, y);
                    } else {
                        inputs.push((address as usize, x, y));
                    }
                }
            }
        }
        for (address, x, y) in inputs {
            network[address].add_input(x);
            network[address].add_input(y);
        }
        if network.iter().all(|computer| computer.polling) {
            for computer in network.iter_mut() {
                computer.clear_inputs();
            }
            if !sent_ys.is_empty() && nat_packet.1 == *sent_ys.iter().last().unwrap() {
                return nat_packet.1;
            } else {
                sent_ys.push(nat_packet.1);
            }
            network[0].add_input(nat_packet.0);
            network[0].add_input(nat_packet.1);
        }
    }
}

fn solve(memory: &Vec<i64>) -> (i64, i64) {
    (part1(memory), part2(memory))
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

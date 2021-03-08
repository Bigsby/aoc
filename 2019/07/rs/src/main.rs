use itertools::Itertools;
use std::cell::RefCell;
use std::collections::VecDeque;
use std::sync::mpsc::{channel, Sender};

type Message = (usize, i32);

pub struct IntCodeComputer {
    memory: RefCell<Vec<i32>>,
    input: RefCell<VecDeque<i32>>,
    output: RefCell<VecDeque<i32>>,
    pointer: usize,
    pub running: bool,
    index: usize,
    sender: Sender<Message>,
}

impl IntCodeComputer {
    pub fn new(memory: &Vec<i32>, input: Vec<i32>, index: usize, sender: Sender<Message>) -> IntCodeComputer {
        IntCodeComputer {
            memory: RefCell::new(memory.clone()),
            input: RefCell::new(VecDeque::from(input)),
            output: RefCell::new(VecDeque::new()),
            pointer: 0,
            running: true,
            index,
            sender,
        }
    }

    pub fn run(&mut self) -> i32 {
        while self.tick() {}
        self.output.borrow_mut().pop_front().unwrap()
    }

    fn get_parameter(&self, offset: i32, mode: i32) -> i32 {
        let value = self.memory.borrow()[self.pointer + offset as usize];
        match mode {
            0 => self.memory.borrow()[value as usize], // POSITION
            1 => value,                                // IMMEDIATE
            _ => {
                panic!("Unrecognized parameter mode '{}'", mode);
            }
        }
    }

    fn add_input(&mut self, value: i32) {
        self.input.borrow_mut().push_back(value);
    }

    fn get_address(&self, offset: i32) -> usize {
        self.memory.borrow()[self.pointer + offset as usize] as usize
    }

    fn tick(&mut self) -> bool {
        if !self.running {
            return false;
        }
        let instruction = self.memory.borrow()[self.pointer];
        let (opcode, p1_mode, p2_mode) = (
            instruction % 100,
            (instruction / 100) % 10,
            (instruction / 1000) % 10,
        );
        match opcode {
            1 => {
                // ADD
                let address = self.get_address(3);
                self.memory.borrow_mut()[address] =
                    self.get_parameter(1, p1_mode) + self.get_parameter(2, p2_mode);
                self.pointer += 4;
            }
            2 => {
                // MUL
                let address = self.get_address(3);
                self.memory.borrow_mut()[address] =
                    self.get_parameter(1, p1_mode) * self.get_parameter(2, p2_mode);
                self.pointer += 4;
            }
            3 => {
                // INPUT
                if let Some(input) = self.input.borrow_mut().pop_front() {
                    let address = self.get_address(1);
                    self.memory.borrow_mut()[address] = input;
                    self.pointer += 2;
                }
            }
            4 => {
                // OUTPUT
                let value = self.get_parameter(1, p1_mode);
                if let Err(_) = self.sender.send((self.index, value)) {
                    panic!("Error sending message.");
                }
                self.output
                    .borrow_mut()
                    .push_back(value);
                self.pointer += 2;
            }
            5 => {
                // JMP_TRUE
                if self.get_parameter(1, p1_mode) != 0 {
                    self.pointer = self.get_parameter(2, p2_mode) as usize;
                } else {
                    self.pointer += 3;
                }
            }
            6 => {
                // JMP_FALSE
                if self.get_parameter(1, p1_mode) == 0 {
                    self.pointer = self.get_parameter(2, p2_mode) as usize;
                } else {
                    self.pointer += 3;
                }
            }
            7 => {
                // LESS_THAN
                let address = self.get_address(3);
                self.memory.borrow_mut()[address] =
                    if self.get_parameter(1, p1_mode) < self.get_parameter(2, p2_mode) {
                        1
                    } else {
                        0
                    };
                self.pointer += 4;
            }
            8 => {
                // EQUALS
                let address = self.get_address(3);
                self.memory.borrow_mut()[address] =
                    if self.get_parameter(1, p1_mode) == self.get_parameter(2, p2_mode) {
                        1
                    } else {
                        0
                    };
                self.pointer += 4;
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

fn run_phases_permutation(memory: &Vec<i32>, phases: Vec<i32>) -> i32 {
    let (sender, _receiver) = channel();
    let mut output = 0;
    for phase in &phases {
        output = IntCodeComputer::new(memory, vec![*phase, output], 0, sender.clone()).run();
    }
    output
}

fn run_feedback_phases_permutation(memory: &Vec<i32>, phases: &Vec<i32>) -> i32 {
    let (sender, receiver) = channel();
    let mut amplifiers: Vec<IntCodeComputer> = phases.into_iter()
        .enumerate()
        .map(|(index, phase)| IntCodeComputer::new(memory, vec![*phase], index, sender.clone())).collect();
    amplifiers[0].add_input(0);
    let mut last_output = 0;
    while amplifiers.iter().any(|ammplifier| ammplifier.running) {
        for amplifier in amplifiers.iter_mut() {
            amplifier.tick();
        }
        let mut message = receiver.try_recv();
        while message.is_ok() {
            let (sender_id, value) = message.unwrap();
            amplifiers[(sender_id + 1) % 5].add_input(value);
            if sender_id == 4 {
                last_output = value;
            }
            message = receiver.try_recv();
        }
    };
    last_output
}


fn solve(memory: &Vec<i32>) -> (i32, i32) {
    (
        (0..5)
            .into_iter()
            .permutations(5)
            .map(|phases| run_phases_permutation(memory, phases))
            .max()
            .unwrap(),
        (5..10)
            .into_iter()
            .permutations(5)
            .map(|phases| run_feedback_phases_permutation(memory, &phases))
            .max()
            .unwrap(),
    )
}

fn get_input(file_path: &String) -> Vec<i32> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split(',')
        .map(|i| i.parse().unwrap())
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

use std::env;
use std::fs;
use std::time::{Instant};
use std::cell::RefCell;

pub struct IntCodeComputer {
    memory: RefCell<Vec<i32>>,
    pointer: usize,
    running: bool,
}

impl IntCodeComputer {
    pub fn new(memory: &Vec<i32>) -> IntCodeComputer {
        IntCodeComputer {
            memory: RefCell::new(memory.clone()),
            pointer: 0,
            running: true
        }
    }

    pub fn run(&mut self) -> i32 {
        while self.running {
            self.tick();
        }
        self.memory.borrow()[0]
    }

    fn get_parameter(&self, offset: i32) -> i32 {
        self.memory.borrow()[self.memory.borrow()[self.pointer + offset as usize] as usize]
    }

    fn get_address(&self, offset: i32) -> usize {
        self.memory.borrow()[self.pointer + offset as usize] as usize
    }

    fn tick(&mut self) {
        if !self.running {
            return
        }
        let opcode = self.memory.borrow()[self.pointer];
        match opcode {
            1 => { // ADD
                let address = self.get_address(3);
                self.memory.borrow_mut()[address] = self.get_parameter(1) + self.get_parameter(2);
                self.pointer += 4;
            },
            2 => { // MUL
                let address = self.get_address(3);
                self.memory.borrow_mut()[address] = self.get_parameter(1) * self.get_parameter(2);
                self.pointer += 4;
            },
            99 => { // HALT
                self.running = false;  
            }
            _ => panic!("Unknown instruction {} {}", self.pointer, opcode)
        }
    }
}

fn run_program(memory: &Vec<i32>, noun: i32, verb: i32) -> i32 {
    let mut memory = memory.clone();
    memory[1] = noun;
    memory[2] = verb;
    IntCodeComputer::new(&memory).run()
}

const TARGET_VALUE: i32 = 19690720;
fn part2(memory: &Vec<i32>) -> i32 {
    for noun in 0..100 {
        for verb in 0..100 {
            if run_program(memory, noun, verb) == TARGET_VALUE {
                return 100 * noun + verb
            }
        }
    };
    panic!("Target value not found")
}

fn solve(memory: &Vec<i32>) -> (i32, i32) {
    (run_program(&memory, 12, 2), part2(memory))
}

fn get_input(file_path: &String) -> Vec<i32> {
    fs::read_to_string(file_path).expect("Error reading input file!")
        .split(',')
        .map(|i| i.trim().parse().unwrap())
        .collect()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Please, add input file path as parameter");
    }
    let now = Instant::now();
    let (part1_result, part2_result) = solve(&get_input(&args[1]));
    println!("P1: {}", part1_result);
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:?}", now.elapsed().as_secs_f32());
}
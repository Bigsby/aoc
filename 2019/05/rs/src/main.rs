use std::cell::RefCell;

pub struct IntCodeComputer {
    memory: RefCell<Vec<i32>>,
    input: i32,
    output: i32,
    pointer: usize,
    running: bool,
}

impl IntCodeComputer {
    pub fn new(memory: &Vec<i32>, input: i32) -> IntCodeComputer {
        IntCodeComputer {
            memory: RefCell::new(memory.clone()),
            input,
            output: 0,
            pointer: 0,
            running: true
        }
    }

    pub fn run(&mut self) -> i32 {
        while self.running {
            self.tick();
        }
        self.output
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

    fn get_address(&self, offset: i32) -> usize {
        self.memory.borrow()[self.pointer + offset as usize] as usize
    }

    fn tick(&mut self) {
        if !self.running {
            return
        }
        let instruction = self.memory.borrow()[self.pointer];
        let (opcode, p1_mode, p2_mode) =  (instruction % 100, (instruction / 100) % 10, (instruction / 1000) % 10);
        match opcode {
            1 => { // ADD
                let address = self.get_address(3);
                self.memory.borrow_mut()[address] = self.get_parameter(1, p1_mode) + self.get_parameter(2, p2_mode);
                self.pointer += 4;
            },
            2 => { // MUL
                let address = self.get_address(3);
                self.memory.borrow_mut()[address] = self.get_parameter(1, p1_mode) * self.get_parameter(2, p2_mode);
                self.pointer += 4;
            },
            3 => { // INPUT
                let address = self.get_address(3);
                self.memory.borrow_mut()[address] = self.input;
                self.pointer += 2;
            },
            4 => { // OUTPUT
                self.output = self.get_parameter(1, p1_mode);
                self.pointer += 2;
            },
            5 => { // JMP_TRUE
                if self.get_parameter(1, p1_mode) != 0 {
                    self.pointer = self.get_parameter(2, p2_mode) as usize;
                } else {
                    self.pointer += 3;
                }
            },
            6 => { // JMP_FALSE
                if self.get_parameter(1, p1_mode) == 0 {
                    self.pointer = self.get_parameter(2, p2_mode) as usize;
                } else {
                    self.pointer += 3;
                }
            },
            7 => { // LESS_THAN
                let address = self.get_address(3);
                self.memory.borrow_mut()[address] = if self.get_parameter(1, p1_mode) < self.get_parameter(2, p2_mode) { 1 } else { 0 };
                self.pointer += 4;
            },
            8 => { // EQUALS
                let address = self.get_address(3);
                self.memory.borrow_mut()[address] = if self.get_parameter(1, p1_mode) == self.get_parameter(2, p2_mode) { 1 } else { 0 };
                self.pointer += 4;
            },
            99 => { // HALT
                self.running = false;  
            },
            _ => panic!("Unknown instruction {} {}", self.pointer, opcode)
        }
    }
}

fn solve(memory: &Vec<i32>) -> (i32, i32) {
    (
        IntCodeComputer::new(memory, 1).run(),
        IntCodeComputer::new(memory, 5).run()
    )
}

fn get_input(file_path: &String) -> Vec<i32> {
    std::fs::read_to_string(file_path).expect("Error reading input file!")
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
    println!("Time: {:7}", now.elapsed().as_secs_f32());
}

use core::cell::RefCell;
use regex::Regex;
use std::collections::HashMap;

pub enum Instruction {
    Mask(String),
    Memory(u64, u64),
}

pub struct Computer {
    memory: RefCell<HashMap<u64, u64>>,
    mask: String,
    mask_value: bool,
    mask_memory: bool,
}

impl Computer {
    fn new(mask_value: bool) -> Computer {
        Computer {
            memory: RefCell::new(HashMap::new()),
            mask: String::from_utf8(vec![b'X'; 1 << 5]).unwrap(),
            mask_value,
            mask_memory: !mask_value,
        }
    }

    pub fn new_value() -> Computer {
        Computer::new(true)
    }

    pub fn new_memory() -> Computer {
        Computer::new(false)
    }

    pub fn run_instruction(&mut self, instruction: &Instruction) {
        match instruction {
            Instruction::Mask(mask) => {
                self.mask = mask.clone();
            }
            Instruction::Memory(location, value) => {
                let value = self.get_value(*value);
                for location in self.get_memory_locations(*location) {
                    *self.memory.borrow_mut().entry(location).or_insert(0) = value;
                }
            }
        }
    }

    pub fn get_memory_sum(&self) -> u64 {
        self.memory.borrow().values().sum()
    }

    fn get_or_mask(&self) -> u64 {
        u64::from_str_radix(self.mask.replace("X", "0").as_str(), 2).unwrap()
    }

    fn get_and_mask(&self) -> u64 {
        u64::from_str_radix(self.mask.replace("X", "1").as_str(), 2).unwrap()
    }

    fn get_memory_locations(&self, location: u64) -> Vec<u64> {
        let mut locations = Vec::new();
        if !self.mask_memory {
            locations.push(location);
            return locations;
        }
        let location = location | self.get_or_mask();
        let mask_bit_offset = self.mask.len() - 1;
        let flip_bits: Vec<u64> = self
            .mask
            .chars()
            .enumerate()
            .filter(|(_, c)| *c == 'X')
            .map(|(index, _)| (mask_bit_offset - index) as u64)
            .collect();
        for occurence in 0..1 << flip_bits.len() {
            let mut current_location = location;
            for (index, flip_bit) in flip_bits.iter().enumerate() {
                current_location &= !(1 << flip_bit);
                let new_bit = ((1 << index) & occurence) >> index;
                current_location |= new_bit << flip_bit;
                locations.push(current_location);
            }
        }
        locations
    }

    fn get_value(&self, value: u64) -> u64 {
        if !self.mask_value {
            value
        } else {
            (value | self.get_or_mask()) & self.get_and_mask()
        }
    }
}

fn run_computer(computer: &mut Computer, instructions: &Vec<Instruction>) -> u64 {
    for instruction in instructions {
        computer.run_instruction(instruction);
    }
    computer.get_memory_sum()
}

fn solve(instructions: &Vec<Instruction>) -> (u64, u64) {
    let _c = Computer::new(false);
    (
        run_computer(&mut Computer::new_value(), instructions),
        run_computer(&mut Computer::new_memory(), instructions),
    )
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    let mask_regex = Regex::new(r"^mask\s=\s(?P<mask>[X01]+)$").unwrap();
    let memory_regex = Regex::new(r"^mem\[(?P<location>[\d]+)]\s=\s(?P<value>[\d]+)$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            if let Some(cap) = mask_regex.captures(line) {
                return Instruction::Mask(String::from(cap.name("mask").unwrap().as_str()));
            } else if let Some(cap) = memory_regex.captures(line) {
                return Instruction::Memory(
                    cap.name("location").unwrap().as_str().parse().unwrap(),
                    cap.name("value").unwrap().as_str().parse().unwrap(),
                );
            } else {
                panic!("Unrecognized instruction '{}'", line)
            }
        })
        .collect()
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

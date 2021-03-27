use regex::Regex;
use std::collections::{HashMap, HashSet};

type Registers = [i32; 4];
type Operation = (i32, usize, usize, usize);
type Record = (Registers, Operation, Registers);

static MNEMONICS: &'static [&'static str] = &[
    "addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri",
    "gtrr", "eqir", "eqri", "eqrr",
];

fn run_operation(registers: &Registers, operation: &Operation, mnemonic: &str) -> Registers {
    let (_, a, b, c) = operation;
    let mut result: Registers = registers.clone();
    result[*c] = match mnemonic {
        "addr" => registers[*a] + registers[*b],
        "addi" => registers[*a] + *b as i32,
        "mulr" => registers[*a] * registers[*b],
        "muli" => registers[*a] * *b as i32,
        "banr" => registers[*a] & registers[*b],
        "bani" => registers[*a] & *b as i32,
        "borr" => registers[*a] | registers[*b],
        "bori" => registers[*a] | *b as i32,
        "setr" => registers[*a],
        "seti" => *a as i32,
        "gtir" => {
            if *a as i32 > registers[*b] {
                1
            } else {
                0
            }
        }
        "gtri" => {
            if registers[*a] > *b as i32 {
                1
            } else {
                0
            }
        }
        "gtrr" => {
            if registers[*a] > registers[*b] {
                1
            } else {
                0
            }
        }
        "eqir" => {
            if *a as i32 == registers[*b] {
                1
            } else {
                0
            }
        }
        "eqri" => {
            if registers[*a] == *b as i32 {
                1
            } else {
                0
            }
        }
        "eqrr" => {
            if registers[*a] == registers[*b] {
                1
            } else {
                0
            }
        }
        _ => {
            panic!("Uknown mnemonic '{}'", mnemonic)
        }
    };
    result
}

fn test_record(
    before: &Registers,
    operation: &Operation,
    after: &Registers,
    opcodes: &mut HashMap<usize, HashSet<i32>>,
) -> usize {
    let mut count = 0;
    let (opcode, _, _, _) = operation;
    for mnemonic_index in 0..MNEMONICS.len() {
        if *after == run_operation(before, operation, MNEMONICS[mnemonic_index]) {
            if !opcodes.get(&mnemonic_index).unwrap().contains(&-opcode) {
                opcodes.get_mut(&mnemonic_index).unwrap().insert(*opcode);
            }
            count += 1;
        } else if opcodes.get(&mnemonic_index).unwrap().contains(&opcode) {
            opcodes.get_mut(&mnemonic_index).unwrap().remove(&opcode);
            opcodes.get_mut(&mnemonic_index).unwrap().insert(-opcode);
        }
    }
    count
}

fn solve(puzzle_input: &(Vec<Record>, Vec<Operation>)) -> (usize, i32) {
    let (records, program) = puzzle_input;
    let mut opcodes: HashMap<usize, HashSet<i32>> = (0..MNEMONICS.len())
        .map(|index| (index, HashSet::new()))
        .collect();
    let mut three_or_more = 0;
    for (before, operation, after) in records {
        if test_record(before, operation, after, &mut opcodes) >= 3 {
            three_or_more += 1;
        }
    }
    println!("{:?}", opcodes);
    for valid in opcodes.values_mut() {
        valid.retain(|v| v >= &0);
    }
    while opcodes.iter().any(|(_, valid)| valid.len() > 1) {
        let single_valid: Vec<i32> = opcodes
            .iter()
            .filter(|(_, valid)| valid.len() == 1)
            .map(|(_, valid)| *valid.iter().next().unwrap())
            .collect();
        for (_, valid) in opcodes.iter_mut() {
            if valid.len() > 1 {
                for single in &single_valid {
                    valid.remove(&single);
                }
            }
        }
    }
    println!("{:?}", opcodes);
    let ops: HashMap<i32, usize> = opcodes
        .into_iter()
        .map(|(index, valid)| (*valid.iter().next().unwrap(), index))
        .collect();
    println!("{:?}", ops);
    let mut registers = [0; 4];
    for operation in program {
        registers = run_operation(
            &registers,
            operation,
            MNEMONICS[*ops.get(&operation.0).unwrap()],
        );
    }
    (three_or_more, registers[0])
}

fn get_input(file_path: &String) -> (Vec<Record>, Vec<Operation>) {
    let record_regex = Regex::new(
        r"Before: \[(?P<b0>\d+), (?P<b1>\d+), (?P<b2>\d+), (?P<b3>\d+)]\n(?P<opCode>\d+) (?P<A>\d) (?P<B>\d) (?P<C>\d)\nAfter:  \[(?P<a0>\d+), (?P<a1>\d+), (?P<a2>\d+), (?P<a3>\d+)]").unwrap();
    let operation_regex = Regex::new(r"(?P<opCode>\d+) (?P<A>\d) (?P<B>\d) (?P<C>\d)").unwrap();
    let split: Vec<String> = std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split("\n\n\n\n")
        .map(|s| String::from(s))
        .collect();
    let mut records = Vec::new();
    for cap in record_regex.captures_iter(split[0].as_str()) {
        records.push((
            [
                cap.name("b0").unwrap().as_str().parse().unwrap(),
                cap.name("b1").unwrap().as_str().parse().unwrap(),
                cap.name("b2").unwrap().as_str().parse().unwrap(),
                cap.name("b3").unwrap().as_str().parse().unwrap(),
            ],
            (
                cap.name("opCode").unwrap().as_str().parse().unwrap(),
                cap.name("A").unwrap().as_str().parse().unwrap(),
                cap.name("B").unwrap().as_str().parse().unwrap(),
                cap.name("C").unwrap().as_str().parse().unwrap(),
            ),
            [
                cap.name("a0").unwrap().as_str().parse().unwrap(),
                cap.name("a1").unwrap().as_str().parse().unwrap(),
                cap.name("a2").unwrap().as_str().parse().unwrap(),
                cap.name("a3").unwrap().as_str().parse().unwrap(),
            ],
        ))
    }
    let mut operations = Vec::new();
    for cap in operation_regex.captures_iter(split[1].as_str()) {
        operations.push((
            cap.name("opCode").unwrap().as_str().parse().unwrap(),
            cap.name("A").unwrap().as_str().parse().unwrap(),
            cap.name("B").unwrap().as_str().parse().unwrap(),
            cap.name("C").unwrap().as_str().parse().unwrap(),
        ));
    }

    (records, operations)
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

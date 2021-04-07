use regex::Regex;
use std::collections::HashMap;

type Registers = [i32; 6];
type Operation = (String, usize, usize, usize);

fn run_operation(registers: &Registers, operation: &Operation) -> Registers {
    let (mnemonic, a, b, c) = operation;
    let mut result: Registers = registers.clone();
    result[*c] = match mnemonic.as_str() {
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

fn part1(data: &(usize, Vec<Operation>)) -> i32 {
    let (ip, operations) = data;
    let mut registers: Registers = [0; 6];
    while registers[*ip] < operations.len() as i32 {
        registers = run_operation(&registers, &operations[registers[*ip] as usize]);
        registers[*ip] += 1;
    }
    return registers[0];
}

fn get_divisors(number: i32) -> Vec<i32> {
    let mut result = Vec::new();
    let mut large_divisors = Vec::new();
    for i in 1..(number as f32).sqrt() as i32 + 1 {
        if number % i == 0 {
            result.push(i);
            if i * i != number {
                large_divisors.push(number / i);
            }
        }
    }
    large_divisors.reverse();
    for divisor in large_divisors {
        result.push(divisor);
    }
    result
}

fn part2(data: &(usize, Vec<Operation>)) -> i32 {
    let value_register: HashMap<usize, usize> = vec![(4, 1), (3, 2)].into_iter().collect();
    let (ip, operations) = data;
    let mut registers: Registers = [0; 6];
    registers[0] = 1;
    while registers[*ip] != 1 {
        registers = run_operation(&registers, &operations[registers[*ip] as usize]);
        registers[*ip] += 1;
    }
    get_divisors(registers[*value_register.get(ip).unwrap()])
        .into_iter()
        .sum()
}

fn solve(data: &(usize, Vec<Operation>)) -> (i32, i32) {
    (part1(data), part2(data))
}

fn get_input(file_path: &String) -> (usize, Vec<Operation>) {
    let operation_regex =
        Regex::new(r"^(?P<mnemonic>\w+) (?P<A>\d+) (?P<B>\d+) (?P<C>\d+)$").unwrap();
    let lines = std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|s| String::from(s))
        .collect::<Vec<String>>();
    (
        lines[0].split(" ").collect::<Vec<&str>>()[1]
            .parse()
            .unwrap(),
        lines[1..]
            .iter()
            .map(|line| {
                operation_regex
                    .captures(line)
                    .map(|cap| {
                        (
                            String::from(cap.name("mnemonic").unwrap().as_str()),
                            cap.name("A").unwrap().as_str().parse().unwrap(),
                            cap.name("B").unwrap().as_str().parse().unwrap(),
                            cap.name("C").unwrap().as_str().parse().unwrap(),
                        )
                    })
                    .unwrap()
            })
            .collect(),
    )
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

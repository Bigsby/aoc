use std::collections::HashMap;

enum Instruction {
    CpyRegister(u8, u8),
    CpyValue(i32, u8),
    Inc(u8),
    Dec(u8),
    Jnz(i32),
    JnzRegister(i32, u8),
}

fn run_instructions(instructions: &Vec<Instruction>, inputs: HashMap<u8, i32>) -> i32 {
    let mut registers: HashMap<u8, i32> = vec![b'a', b'b', b'c', b'd']
        .into_iter()
        .map(|register| (register, 0))
        .collect();
    for (key, value) in inputs {
        *registers.entry(key).or_insert(0) = value;
    }
    let mut pointer = 0;
    while pointer < instructions.len() {
        let instruction = &instructions[pointer];
        match instruction {
            Instruction::CpyRegister(source, target) => {
                *registers.entry(*target).or_insert(0) = *registers.get(source).unwrap();
                pointer += 1;
            }
            Instruction::CpyValue(value, target) => {
                *registers.entry(*target).or_insert(0) = *value;
                pointer += 1;
            }
            Instruction::Inc(register) => {
                *registers.entry(*register).or_insert(0) += 1;
                pointer += 1;
            }
            Instruction::Dec(register) => {
                *registers.entry(*register).or_insert(0) -= 1;
                pointer += 1;
            }
            Instruction::Jnz(jump) => {
                pointer = (pointer as i32 + jump) as usize;
            }
            Instruction::JnzRegister(jump, register) => {
                if *registers.get(register).unwrap() != 0 {
                    pointer = (pointer as i32 + jump) as usize;
                } else {
                    pointer += 1;
                }
            }
        }
    }
    *registers.get(&b'a').unwrap()
}

fn solve(instructions: &Vec<Instruction>) -> (i32, i32) {
    (
        run_instructions(instructions, HashMap::new()),
        run_instructions(instructions, vec![(b'c', 1)].into_iter().collect()),
    )
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let split: Vec<String> = line
                .split(" ")
                .map(|part| String::from(part.trim()))
                .collect();
            match split[0].as_str() {
                "cpy" => {
                    let (source_param, target_param) = (&split[1], &split[2]);
                    if let Ok(value) = source_param.parse::<i32>() {
                        Instruction::CpyValue(
                            value,
                            target_param.chars().into_iter().next().unwrap() as u8,
                        )
                    } else {
                        Instruction::CpyRegister(
                            source_param.chars().into_iter().next().unwrap() as u8,
                            target_param.chars().into_iter().next().unwrap() as u8,
                        )
                    }
                }
                "inc" => Instruction::Inc(split[1].chars().into_iter().next().unwrap() as u8),
                "dec" => Instruction::Dec(split[1].chars().into_iter().next().unwrap() as u8),
                "jnz" => {
                    let (register, jump) = (&split[1], &split[2]);
                    if let Ok(_) = register.parse::<usize>() {
                        Instruction::Jnz(jump.parse::<i32>().unwrap())
                    } else {
                        Instruction::JnzRegister(
                            jump.parse::<i32>().unwrap(),
                            register.chars().into_iter().next().unwrap() as u8,
                        )
                    }
                }
                _ => panic!("Unkown instruvction {}", split[0]),
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

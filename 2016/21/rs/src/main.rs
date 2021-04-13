use std::collections::VecDeque;

#[derive(Copy, Clone)]
enum Instruction {
    SwapPosition(usize, usize),
    SwapLetter(u8, u8),
    RotateLeft(usize),
    RotateRight(usize),
    RotateLetter(u8),
    Reverse(usize, usize),
    Move(usize, usize),
}

fn process(start: &str, instructions: &Vec<Instruction>, reverse: bool) -> String {
    let mut password: VecDeque<u8> = start.chars().map(|c| c as u8).collect();
    let mut instructions = instructions.clone();
    if reverse {
        instructions.reverse();
    }
    for instruction in instructions {
        use Instruction::*;
        match instruction {
            SwapPosition(a, b) => {
                let old_a = password[a];
                password[a] = password[b];
                password[b] = old_a;
            }
            SwapLetter(a, b) => {
                let index_of_a = password.iter().position(|c| *c == a).unwrap();
                let index_of_b = password.iter().position(|c| *c == b).unwrap();
                let old_a = password[index_of_a];
                password[index_of_a] = password[index_of_b];
                password[index_of_b] = old_a;
            }
            RotateLeft(a) => {
                if reverse {
                    password.rotate_right(a);
                } else {
                    password.rotate_left(a);
                }
            }
            RotateRight(a) => {
                if reverse {
                    password.rotate_left(a);
                } else {
                    password.rotate_right(a);
                }
            }
            RotateLetter(a) => {
                let index_of_a = password.iter().position(|c| *c == a).unwrap();
                if reverse {
                    password.rotate_left(
                        index_of_a / 2
                            + (if index_of_a % 2 == 1 || index_of_a == 0 {
                                1
                            } else {
                                5
                            }),
                    );
                } else {
                    password.rotate_right(
                        (index_of_a + 1 + (if index_of_a >= 4 { 1 } else { 0 })) % password.len(),
                    );
                }
            }
            Reverse(a, b) => {
                let mut prefix: Vec<u8> = password.range(..a).copied().collect();
                let mut middle: Vec<u8> = password.range(a..b + 1).copied().collect();
                let mut suffix: Vec<u8> = password.range(b + 1..).copied().collect();
                middle.reverse();
                prefix.append(&mut middle);
                prefix.append(&mut suffix);
                password = prefix.into_iter().collect();
            }
            Move(a, b) => {
                let (origin, destination) = if reverse { (b, a) } else { (a, b) };
                let letter_to_move = password[origin];
                password.remove(origin);
                password.insert(destination, letter_to_move);
            }
        }
    }
    password.iter().map(|c| *c as char).collect()
}

fn solve(instructions: &Vec<Instruction>) -> (String, String) {
    (
        process("abcdefgh", instructions, false),
        process("fbgdceah", instructions, true),
    )
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    use Instruction::*;
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            if line.starts_with("swap position") {
                SwapPosition(
                    line[14..15].parse().unwrap(),
                    line[line.len() - 1..line.len()].parse().unwrap(),
                )
            } else if line.starts_with("swap letter") {
                SwapLetter(
                    line.chars().nth(12).unwrap() as u8,
                    line.chars().last().unwrap() as u8,
                )
            } else if line.starts_with("rotate left") {
                RotateLeft(line[12..13].parse().unwrap())
            } else if line.starts_with("rotate right") {
                RotateRight(line[13..14].parse().unwrap())
            } else if line.starts_with("rotate based") {
                RotateLetter(line.chars().last().unwrap() as u8)
            } else if line.starts_with("reverse") {
                Reverse(
                    line[18..19].parse().unwrap(),
                    line[line.len() - 1..line.len()].parse().unwrap(),
                )
            } else if line.starts_with("move") {
                Move(
                    line[14..15].parse().unwrap(),
                    line[line.len() - 1..line.len()].parse().unwrap(),
                )
            } else {
                panic!("Uknown instruction '{}'", line);
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

use regex::Regex;
use std::collections::HashMap;

struct Instruction {
    action: u32,
    x_start: u32,
    y_start: u32,
    x_end: u32,
    y_end: u32,
}

const MATRIX_SIDE: u32 = 1000;
const TURN_ON: u32 = 0;
const TOGGLE: u32 = 1;
const TURN_OFF: u32 = 2;

fn run_matrix<T>(instructions: &Vec<Instruction>, update_func: T) -> u32
where
    T: Fn(u32, u32) -> u32,
{
    let mut matrix: [u32; (MATRIX_SIDE * MATRIX_SIDE) as usize] =
        [0; (MATRIX_SIDE * MATRIX_SIDE) as usize];
    for instruction in instructions {
        for x in instruction.x_start..(instruction.x_end + 1) {
            for y in instruction.y_start..(instruction.y_end + 1) {
                let position = x + y * MATRIX_SIDE;
                matrix[position as usize] =
                    update_func(instruction.action, matrix[position as usize]);
            }
        }
    }
    matrix.iter().sum()
}

fn solve(instructions: &Vec<Instruction>) -> (u32, u32) {
    (
        run_matrix(instructions, |action, value| match action {
            TURN_ON => 1,
            TOGGLE => {
                if value == 1 {
                    0
                } else {
                    1
                }
            }
            TURN_OFF => 0,
            _ => panic!("Uknow action '{}'", action),
        }),
        run_matrix(instructions, |action, value| match action {
            TURN_ON => value + 1,
            TOGGLE => value + 2,
            TURN_OFF => {
                if value > 0 {
                    value - 1
                } else {
                    0
                }
            }
            _ => panic!("Uknow action '{}'", action),
        }),
    )
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    let actions: HashMap<&str, u32> = vec![
        ("turn on", TURN_ON),
        ("toggle", TOGGLE),
        ("turn off", TURN_OFF),
    ]
    .into_iter()
    .collect();
    let re = Regex::new(
        r"^(toggle|turn off|turn on)\s(\d{1,3}),(\d{1,3})\sthrough\s(\d{1,3}),(\d{1,3})$",
    )
    .unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            re.captures(line)
                .map(|cap| Instruction {
                    action: actions[cap.get(1).unwrap().as_str()],
                    x_start: cap.get(2).unwrap().as_str().parse().unwrap(),
                    y_start: cap.get(3).unwrap().as_str().parse().unwrap(),
                    x_end: cap.get(4).unwrap().as_str().parse().unwrap(),
                    y_end: cap.get(5).unwrap().as_str().parse().unwrap(),
                })
                .unwrap()
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
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:7}", end);
}

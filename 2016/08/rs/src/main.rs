use std::collections::HashMap;

type Pixel = num::complex::Complex<u32>;

enum Instruction {
    Rect(u32, u32),
    RotateRow(u32, u32),
    RotateColumn(u32, u32),
}

const CHARACTER_WIDTH: u32 = 5;
const SCREEN_WIDTH: u32 = 50;
const SCREEN_HEIGHT: u32 = 6;

struct LetterMap {
    letters: HashMap<u32, char>,
}

impl LetterMap {
    fn new() -> LetterMap {
        LetterMap {
            letters: vec![
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b11110 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'A',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b11100 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b11100 << CHARACTER_WIDTH * 5),
                    'B',
                ),
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'C',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b11100 << CHARACTER_WIDTH * 5),
                    'D',
                ),
                (
                      (0b11110 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b11100 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b11110 << CHARACTER_WIDTH * 5),
                    'E',
                ),
                (
                      (0b11110 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b11100 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b10000 << CHARACTER_WIDTH * 5),
                    'F',
                ),
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b10110 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01110 << CHARACTER_WIDTH * 5),
                    'G',
                ),
                (
                      (0b10010 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b11110 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'H',
                ),
                (
                      (0b01110 << CHARACTER_WIDTH * 0)
                    + (0b00100 << CHARACTER_WIDTH * 1)
                    + (0b00100 << CHARACTER_WIDTH * 2)
                    + (0b00100 << CHARACTER_WIDTH * 3)
                    + (0b00100 << CHARACTER_WIDTH * 4)
                    + (0b01110 << CHARACTER_WIDTH * 5),
                    'I',
                ),
                (
                      (0b00110 << CHARACTER_WIDTH * 0)
                    + (0b00010 << CHARACTER_WIDTH * 1)
                    + (0b00010 << CHARACTER_WIDTH * 2)
                    + (0b00010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'J',
                ),
                (
                      (0b10010 << CHARACTER_WIDTH * 0)
                    + (0b10100 << CHARACTER_WIDTH * 1)
                    + (0b11000 << CHARACTER_WIDTH * 2)
                    + (0b10100 << CHARACTER_WIDTH * 3)
                    + (0b10100 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'K',
                ),
                (
                      (0b10000 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b11110 << CHARACTER_WIDTH * 5),
                    'L',
                ),
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'O',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b11100 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b10000 << CHARACTER_WIDTH * 5),
                    'P',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b11100 << CHARACTER_WIDTH * 3)
                    + (0b10100 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'R',
                ),
                (
                      (0b01110 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b01100 << CHARACTER_WIDTH * 3)
                    + (0b00010 << CHARACTER_WIDTH * 4)
                    + (0b11100 << CHARACTER_WIDTH * 5),
                    'S',
                ),
                (
                      (0b10010 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'U',
                ),
                (
                      (0b10001 << CHARACTER_WIDTH * 0)
                    + (0b10001 << CHARACTER_WIDTH * 1)
                    + (0b01010 << CHARACTER_WIDTH * 2)
                    + (0b00100 << CHARACTER_WIDTH * 3)
                    + (0b00100 << CHARACTER_WIDTH * 4)
                    + (0b00100 << CHARACTER_WIDTH * 5),
                    'Y',
                ),
                (
                      (0b11110 << CHARACTER_WIDTH * 0)
                    + (0b00010 << CHARACTER_WIDTH * 1)
                    + (0b00100 << CHARACTER_WIDTH * 2)
                    + (0b01000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b11110 << CHARACTER_WIDTH * 5),
                    'Z',
                ),
            ]
            .into_iter()
            .collect::<HashMap<u32, char>>(),
        }
    }
    fn get(&self, code: u32) -> char {
        *self.letters.get(&code).unwrap()
    }
}

fn _print_screen(screen: &Vec<Pixel>, width: u32, height: u32) {
    for y in 0..height {
        for x in 0..width {
            print!(
                "{}",
                if screen.contains(&Pixel::new(x, y)) {
                    '#'
                } else {
                    '.'
                }
            )
        }
        println!("");
    }
    println!("");
}

fn run_instructions(instructions: &Vec<Instruction>, width: u32, height: u32) -> Vec<Pixel> {
    let mut screen = Vec::new();
    let mut to_add: Vec<Pixel> = Vec::new();
    let mut to_remove: Vec<Pixel> = Vec::new();
    for instruction in instructions {
        match instruction {
            Instruction::Rect(a, b) => {
                for x in 0..*a {
                    for y in 0..*b {
                        let pixel = Pixel::new(x, y);
                        if !screen.contains(&pixel) {
                            screen.push(pixel);
                        }
                    }
                }
            }
            Instruction::RotateRow(row, shift) => {
                to_remove = Vec::new();
                to_add = Vec::new();
                for pixel in &screen {
                    if pixel.im == *row {
                        to_remove.push(*pixel);
                        to_add.push(Pixel::new((pixel.re + shift) % width, pixel.im));
                    }
                }
            }
            Instruction::RotateColumn(column, shift) => {
                to_remove = Vec::new();
                to_add = Vec::new();
                for pixel in &screen {
                    if pixel.re == *column {
                        to_remove.push(*pixel);
                        to_add.push(Pixel::new(pixel.re, (pixel.im + shift) % height));
                    }
                }
            }
        }
        for pixel in &to_remove {
            if let Some(index) = screen.iter().position(|p| p == pixel) {
                screen.remove(index);
            }
        }
        for pixel in &to_add {
            screen.push(*pixel);
        }
        to_add.clear();
        to_remove.clear();
    }
    screen
}

fn get_character_in_screen(
    screen: &Vec<Pixel>,
    index: u32,
    width: u32,
    height: u32,
    letter_map: &LetterMap,
) -> char {
    let mut screen_value = 0;
    for x in 0..width {
        for y in 0..height {
            if screen.contains(&Pixel::new(width * index + x, y)) {
                screen_value += u32::pow(2, width - 1 - x) << (y * width);
            }
        }
    }
    letter_map.get(screen_value)
}

fn solve(instructions: &Vec<Instruction>) -> (usize, String) {
    let letter_map = LetterMap::new();
    let screen = run_instructions(instructions, SCREEN_WIDTH, SCREEN_HEIGHT);
    (
        screen.len(),
        (0..(SCREEN_WIDTH / CHARACTER_WIDTH))
            .into_iter()
            .map(|index| {
                get_character_in_screen(&screen, index, CHARACTER_WIDTH, SCREEN_HEIGHT, &letter_map)
            })
            .collect::<String>(),
    )
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            if line.starts_with("rect") {
                let split = line[5..].splitn(2, "x").collect::<Vec<&str>>();
                return Instruction::Rect(split[0].parse().unwrap(), split[1].parse().unwrap());
            } else if line.starts_with("rotate row") {
                let split = line[13..].splitn(2, " by ").collect::<Vec<&str>>();
                return Instruction::RotateRow(
                    split[0].parse().unwrap(),
                    split[1].parse().unwrap(),
                );
            } else if line.starts_with("rotate column") {
                let split = line[16..].splitn(2, " by ").collect::<Vec<&str>>();
                return Instruction::RotateColumn(
                    split[0].parse().unwrap(),
                    split[1].parse().unwrap(),
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
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}

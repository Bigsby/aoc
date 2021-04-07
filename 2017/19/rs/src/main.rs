use num::Complex;
use std::collections::HashMap;

type Position = Complex<i32>;
type Tubes = Vec<Position>;
type Letters = HashMap<Position, char>;

fn solve(data: &(Tubes, Letters, Position)) -> (String, usize) {
    const LEFT: Position = Position::new(0, 1);
    const RIGHT: Position = Position::new(0, -1);
    let (tubes, letters, current_position) = data;
    let mut current_position = *current_position;
    let mut path = String::new();
    let mut direction = Position::new(0, 1);
    let mut steps = 0;
    loop {
        steps += 1;
        if let Some(letter) = letters.get(&current_position) {
            path.push(*letter);
        }
        if tubes.contains(&(current_position + direction)) {
            current_position += direction;
        } else if tubes.contains(&(current_position + direction * LEFT)) {
            direction *= LEFT;
            current_position += direction;
        } else if tubes.contains(&(current_position + direction * RIGHT)) {
            direction *= RIGHT;
            current_position += direction;
        } else {
            break;
        }
    }
    (path, steps)
}

fn get_input(file_path: &str) -> (Tubes, Letters, Position) {
    const TUBES: [char; 3] = ['|', '+', '-'];
    let mut tubes = Tubes::new();
    let mut letters = Letters::new();
    let mut start = Position::new(0, 0);
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            let position = Position::new(x as i32, y as i32);
            if TUBES.contains(&c) {
                tubes.push(position);
                if y == 0 {
                    start = position;
                }
            }
            if c >= 'A' && c <= 'Z' {
                letters.insert(position, c);
                tubes.push(position);
            }
        }
    }
    (tubes, letters, start)
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

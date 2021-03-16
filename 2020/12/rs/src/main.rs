use num::complex::Complex;
use std::collections::HashMap;

type Instruction = (char, i32);

fn navigate(
    instructions: &Vec<Instruction>,
    heading: Complex<i32>,
    heading_on_cardinal: bool,
    cardinal_directions: &HashMap<char, Complex<i32>>,
    rotations: &HashMap<char, Complex<i32>>,
) -> i32 {
    let mut position = Complex::new(0, 0);
    let mut heading = heading;
    for (direction, value) in instructions {
        if cardinal_directions.contains_key(&direction) {
            if heading_on_cardinal {
                heading += cardinal_directions[direction] * value;
            } else {
                position += cardinal_directions[direction] * value;
            }
        } else if rotations.contains_key(&direction) {
            heading *= num::pow(rotations[direction], (*value as usize) / 90);
        } else if *direction == 'F' {
            position += heading * value;
        }
    }
    i32::abs(position.re) + i32::abs(position.im)
}

fn solve(instructions: &Vec<Instruction>) -> (i32, i32) {
    let cardinal_directions: HashMap<char, Complex<i32>> = vec![
        ('N', Complex::new(0, 1)),
        ('S', Complex::new(0, -1)),
        ('E', Complex::new(1, 0)),
        ('W', Complex::new(-1, 0)),
    ]
    .into_iter()
    .collect();
    let rotations: HashMap<char, Complex<i32>> =
        vec![('L', Complex::new(0, 1)), ('R', Complex::new(0, -1))]
            .into_iter()
            .collect();
    (
        navigate(
            instructions,
            Complex::new(1, 0),
            false,
            &cardinal_directions,
            &rotations,
        ),
        navigate(
            instructions,
            Complex::new(10, 1),
            true,
            &cardinal_directions,
            &rotations,
        ),
    )
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let chars: Vec<char> = line.chars().collect();
            (
                *chars.first().unwrap(),
                chars[1..].iter().collect::<String>().parse().unwrap(),
            )
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

use num::complex::Complex;
use std::collections::HashMap;
use std::env;
use std::fs;
use std::time::Instant;

macro_rules! c {
    ($x: expr, $y: expr) => {
        Complex::new($x, $y)
    };
}

fn part1(target: &i32) -> i32 {
    let side = (*target as f64).sqrt().floor() as i32 + 1;
    let mut past_last_square = target - (side - 1).pow(2);
    let half_side = side / 2;
    if past_last_square >= side {
        past_last_square -= side;
    }
    let offset_to_middle = (half_side - past_last_square).abs();
    half_side + offset_to_middle
}

fn get_sum_for_neighbors(
    directions: &Vec<Complex<i32>>,
    grid: &HashMap<Complex<i32>, i32>,
    position: &Complex<i32>,
) -> i32 {
    directions.iter().fold(0i32, |acc, direction| {
        let neighbor = position + direction;
        if grid.contains_key(&neighbor) {
            grid.get(&neighbor).unwrap() + acc
        } else {
            acc
        }
    })
}

fn part2(target: &i32) -> i32 {
    let directions = vec![
        c!(-1, -1), c!(0, -1), c!(1, -1),
        c!(-1,  0),            c!(1,  0),
        c!(-1,  1), c!(0,  1), c!(1,  1),
    ];
    let turn = c!(0, 1);
    let mut grid = HashMap::new();
    let mut position = c!(0, 0);
    grid.insert(position, 1);
    let mut direction = c!(1, 0);
    let mut moves_in_direction = 1;
    loop {
        for _ in 0..2 {
            direction *= turn;
            for _ in 0..moves_in_direction {
                position += direction;
                let new_value = get_sum_for_neighbors(&directions, &grid, &position);
                if new_value > *target {
                    return new_value;
                }
                grid.insert(position, new_value);
            }
        }
        moves_in_direction += 1;
    }
}

fn solve(target: &i32) -> (i32, i32) {
    (part1(target), part2(target))
}

fn get_input(file_path: &String) -> i32 {
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .parse()
        .unwrap()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Please, add input file path as parameter");
    }
    let now = Instant::now();
    let (part1_result, part2_result) = solve(&get_input(&args[1]));
    println!("P1: {}", part1_result);
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:7}", now.elapsed().as_secs_f32());
}

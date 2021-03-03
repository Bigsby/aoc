use num::complex::Complex;
use std::env;
use std::fs;
use std::time::Instant;

type Trees = Vec<Complex<i32>>;

fn print_trees(trees: &Trees) {
    let max_x = trees.iter().map(|p| p.re).max().unwrap() + 1;
    let max_y = trees.iter().map(|p| p.im).max().unwrap() + 1;
    println!("{} {}", max_x, max_y);
    for y in 0..max_y {
        for x in 0..max_x {
            print!(
                "{}",
                if trees.contains(&Complex::new(x, y)) {
                    '#'
                } else {
                    ','
                }
            )
        }
        println!("")
    }
    println!("")
}

fn calculate_trees(trees: &Trees, step: Complex<i32>) -> u32 {
    let mut tree_count = 0;
    let max_x = trees.iter().map(|p| p.re).max().unwrap() + 1;
    let max_y = trees.iter().map(|p| p.im).max().unwrap() + 1;
    let mut position = Complex::new(0, 0);
    while position.im < max_y {
        if trees.contains(&Complex::new(position.re % max_x, position.im)) {
            tree_count += 1;
        }
        position += step;
    }
    tree_count
}

fn solve(trees: &Trees) -> (u32, u32) {
    (
        calculate_trees(trees, Complex::new(3, 1)), 
        vec![
            Complex::new(1, 1),
            Complex::new(3, 1),
            Complex::new(5, 1),
            Complex::new(7, 1),
            Complex::new(1, 2),
        ].iter().fold(1u32, |acc, step| acc * calculate_trees(&trees, *step))
    )
}

fn get_input(file_path: &String) -> Trees {
    let mut trees = vec![];
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
        .for_each(|(y, line)| {
            line.chars()
                .enumerate()
                .filter(|(_, c)| *c == '#')
                .for_each(|(x, _)| trees.push(Complex::new(x as i32, y as i32)))
        });
    trees
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

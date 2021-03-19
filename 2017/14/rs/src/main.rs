use num::complex::Complex;
use std::collections::VecDeque;
use std::fmt::Write;

const MARKS_COUNT: usize = 256;

fn run_lengths(
    marks: &Vec<usize>,
    lenghts: &Vec<usize>,
    current_mark: usize,
    skip: usize,
) -> (Vec<usize>, usize, usize) {
    let mut marks = marks.clone();
    let mut current_mark = current_mark;
    let mut skip = skip;
    for length in lenghts {
        let mut to_reverse = Vec::new();
        let mut reverse_mark = current_mark;
        for _ in 0..*length {
            to_reverse.push(marks[reverse_mark]);
            reverse_mark = (reverse_mark + 1) % MARKS_COUNT;
        }
        reverse_mark = current_mark;
        while let Some(mark) = to_reverse.pop() {
            marks[reverse_mark] = mark;
            reverse_mark = (reverse_mark + 1) % MARKS_COUNT;
        }
        current_mark = (current_mark + length + skip) % MARKS_COUNT;
        skip += 1;
    }
    (marks, current_mark, skip)
}

fn knot_hash(puzzle_input: &str) -> String {
    let suffix = vec![17, 31, 73, 47, 23];
    let mut lengths: Vec<usize> = puzzle_input.chars().map(|c| c as usize).collect();
    lengths.extend(suffix);
    let mut marks: Vec<usize> = (0..MARKS_COUNT).into_iter().collect();
    let mut current_mark = 0;
    let mut skip = 0;
    for _ in 0..64 {
        let result = run_lengths(&marks, &lengths, current_mark, skip);
        marks = result.0;
        current_mark = result.1;
        skip = result.2;
    }
    let dense_hash: Vec<usize> = (0..16)
        .into_iter()
        .map(|index| {
            marks[index * 16..(index + 1) * 16]
                .iter()
                .fold(0, |acc, mark| acc ^ mark)
        })
        .collect();

    let mut result = String::new();
    for byte in dense_hash {
        if let Err(_) = write!(result, "{:02x}", byte) {
            panic!("Error writing hex string");
        }
    }
    result
}

fn get_row_hash_binary_string(key: &str, index: usize) -> String {
    format!(
        "{:128b}",
        u128::from_str_radix(&knot_hash(&format!("{}-{}", key, index)), 16).unwrap()
    )
}

fn find_adjacent(point: Complex<i32>, grid: &Vec<Complex<i32>>) -> Vec<Complex<i32>> {
    let directions = vec![
        Complex::new(0, 1),
        Complex::new(1, 0),
        Complex::new(0, -1),
        Complex::new(-1, 0),
    ];
    let mut visited = Vec::new();
    let mut queue = VecDeque::new();
    queue.push_back(point);
    while let Some(point) = queue.pop_front() {
        visited.push(point);
        for direction in &directions {
            let new_point = point + direction;
            if grid.contains(&new_point)
                && !visited.contains(&new_point)
                && !queue.contains(&new_point)
            {
                queue.push_back(new_point);
            }
        }
    }
    visited
}

fn part2(key: &str) -> usize {
    let mut grid_points = Vec::new();
    for row in 0..128 {
        for (column, c) in get_row_hash_binary_string(key, row).chars().enumerate() {
            if c == '1' {
                grid_points.push(Complex::new(column as i32, row as i32));
            }
        }
    }
    let mut regions = 0;
    while let Some(point) = grid_points.pop() {
        regions += 1;
        for visited in find_adjacent(point, &grid_points) {
            if let Some(adjacent) = grid_points.iter().position(|p| p == &visited) {
                grid_points.remove(adjacent);
            }
        }
    }
    regions
}

fn solve(key: &str) -> (usize, usize) {
    (
        (0..128)
            .into_iter()
            .map(|index| {
                get_row_hash_binary_string(key, index)
                    .chars()
                    .filter(|c| c == &'1')
                    .count()
            })
            .sum::<usize>(),
        part2(key),
    )
}

fn get_input(file_path: &String) -> String {
    String::from(
        std::fs::read_to_string(file_path)
            .expect("Error reading input file!")
            .trim(),
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
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}

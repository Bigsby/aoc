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

fn part1(puzzle_input: &str) -> usize {
    let lengths = puzzle_input
        .split(",")
        .map(|len| len.parse().unwrap())
        .collect();
    let (marks, _, _) = run_lengths(&(0..MARKS_COUNT).into_iter().collect(), &lengths, 0, 0);
    marks[0] * marks[1]
}

fn part2(puzzle_input: &str) -> String {
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

fn solve(puzzle_input: &str) -> (usize, String) {
    (part1(puzzle_input), part2(puzzle_input))
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

use regex::Regex;
use std::collections::VecDeque;

fn solve(puzzle_input: &(usize, usize)) -> (usize, usize) {
    let (elves_count, last_marble) = *puzzle_input;
    let mut part1_score = 0;
    let mut scores = vec![0; elves_count];
    let mut circle = VecDeque::with_capacity(last_marble * 100);
    circle.push_back(0);
    for next_marble in 1..=last_marble * 100 {
        if next_marble == last_marble {
            part1_score = *scores.iter().max().unwrap();
        }
        if next_marble % 23 == 0 {
            for _ in 0..7 {
                let previous = circle.pop_back().unwrap();
                circle.push_front(previous);
            }
            scores[next_marble % elves_count] += next_marble + circle.pop_front().unwrap();
        } else {
            for _ in 0..2 {
                let next = circle.pop_front().unwrap();
                circle.push_back(next);
            }
            circle.push_front(next_marble);
        }
    }
    (part1_score, *scores.iter().max().unwrap())
}

fn get_input(file_path: &String) -> (usize, usize) {
    let re = Regex::new(r"^(?P<players>\d+) players; last marble is worth (?P<last>\d+)").unwrap();
    re.captures(
        std::fs::read_to_string(file_path)
            .expect("Error reading input file!")
            .as_str(),
    )
    .map(|cap| {
        (
            cap.name("players").unwrap().as_str().parse().unwrap(),
            cap.name("last").unwrap().as_str().parse().unwrap(),
        )
    })
    .unwrap()
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

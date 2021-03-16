use std::collections::HashMap;

type State = Vec<i64>;
type Notes = HashMap<i64, bool>;

fn get_state_value(index: i64, state: &State) -> i64 {
    (0..5)
        .into_iter()
        .filter(|i| state.contains(&(i + index - 2)))
        .map(|i| 1 << i)
        .sum()
}

fn run_generations(state: &State, notes: &Notes, generations: i64) -> State {
    let mut generation = 0;
    let mut state: State = state.iter().map(|i| *i).collect();
    while generation < generations {
        let mut new_state = Vec::new();
        for index in (state.iter().min().unwrap() - 2)..(state.iter().max().unwrap() + 2) {
            if let Some(true) = notes.get(&get_state_value(index, &state)) {
                new_state.push(index);
            }
        }
        state = new_state;
        generation += 1;
    }
    state
}

fn part2(state: &State, notes: &Notes) -> i64 {
    let jump = 200i64;
    let target = 5 * i64::pow(10, 10);
    let first_state = run_generations(state, notes, jump);
    let first_sum: i64 = first_state.iter().sum();
    let second_state = run_generations(&first_state, notes, jump);
    let diff: i64 = second_state.into_iter().sum::<i64>() - first_sum;
    first_sum + diff * (target / jump - 1)
}

fn solve(puzzle_input: &(State, Notes)) -> (i64, i64) {
    let (state, notes) = puzzle_input;
    (
        run_generations(state, notes, 20).into_iter().sum(),
        part2(state, notes),
    )
}

fn parse_initial_state(line: &str) -> State {
    line.chars()
        .into_iter()
        .skip(15)
        .enumerate()
        .filter(|(_, c)| *c == '#')
        .map(|(index, _)| index as i64)
        .collect()
}

fn compute_pattern(pattern: &str) -> i64 {
    pattern
        .chars()
        .into_iter()
        .enumerate()
        .filter(|(_, c)| *c == '#')
        .map(|(index, _)| 1 << index as i64)
        .sum()
}

fn parse_note(line: &str) -> (i64, bool) {
    let split: Vec<&str> = line.trim().split(" => ").collect();
    (
        compute_pattern(split[0]),
        split[1].chars().next().unwrap() == '#',
    )
}

fn get_input(file_path: &String) -> (State, Notes) {
    let lines: Vec<String> = std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .into_iter()
        .map(|line| String::from(line))
        .collect();
    (
        parse_initial_state(&lines[0]),
        lines[2..]
            .into_iter()
            .map(|line| parse_note(line))
            .collect(),
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
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}

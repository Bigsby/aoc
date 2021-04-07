use std::collections::VecDeque;

fn part1(elf_count: &usize) -> usize {
    1 + 2 * (elf_count - usize::pow(2, f32::log(*elf_count as f32, 2.0).floor() as u32))
}

fn part2(elf_count: &usize) -> usize {
    let mut first_half: VecDeque<usize> = (1..(*elf_count + 1) / 2 + 1).collect();
    let mut second_half: VecDeque<usize> = ((*elf_count + 1) / 2 + 1..(*elf_count + 1)).collect();
    loop {
        if second_half.len() >= first_half.len() {
            second_half.pop_front();
            if second_half.is_empty() {
                return first_half[0];
            }
        } else {
            first_half.pop_back();
        }
        first_half.push_back(second_half.pop_front().unwrap());
        second_half.push_back(first_half.pop_front().unwrap());
    }
}

fn solve(elf_count: &usize) -> (usize, usize) {
    (part1(elf_count), part2(elf_count))
}

fn get_input(file_path: &String) -> usize {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .parse()
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
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}

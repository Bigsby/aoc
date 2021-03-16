use std::collections::HashMap;

type Scanners = HashMap<u32, u32>;

fn part1(scanners: &Scanners, cycles: &Scanners) -> u32 {
    let mut severity = 0;
    for current_layer in 0..scanners.keys().max().unwrap() + 1 {
        if cycles.contains_key(&current_layer) && current_layer % cycles[&current_layer] == 0 {
            severity += current_layer * scanners[&current_layer];
        }
    }
    severity
}

fn run_packet_until_caught(cycles: &Scanners, offset: u32, max_cycle: u32) -> bool {
    for current_layer in 0..max_cycle {
        if cycles.contains_key(&current_layer)
            && (current_layer + offset) % cycles[&current_layer] == 0
        {
            return false;
        }
    }
    true
}

fn part2(cycles: &Scanners) -> u32 {
    let mut offset = 1;
    let max_cycle = cycles.keys().max().unwrap() + 1;
    while !run_packet_until_caught(cycles, offset, max_cycle) {
        offset += 1
    }
    offset
}

fn solve(scanners: &Scanners) -> (u32, u32) {
    let cycles: Scanners = scanners
        .into_iter()
        .map(|(layer, range)| (*layer, 2 * (range - 1)))
        .collect();
    (part1(scanners, &cycles), part2(&cycles))
}

fn get_input(file_path: &String) -> Scanners {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let split: Vec<&str> = line.split(":").collect();
            (
                split[0].trim().parse().unwrap(),
                split[1].trim().parse().unwrap(),
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

fn solve(numbers: &Vec<usize>) -> (usize, usize) {
    const TURNS: usize = 30_000_000;
    let mut part1_result = 0;
    let mut turn = 0;
    let mut last_number = *numbers.into_iter().last().unwrap();
    let mut occurrences = vec![0; TURNS];
    for number in numbers {
        turn += 1;
        occurrences[*number] = turn;
    }
    while turn < TURNS {
        let last_occurrence = occurrences[last_number];
        occurrences[last_number] = turn;
        if turn == 2020 {
            part1_result = last_number;
        }
        last_number = if last_occurrence != 0 {
            turn - last_occurrence
        } else {
            0
        };
        turn += 1;
    }
    (part1_result, last_number)
}

fn get_input(file_path: &String) -> Vec<usize> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split(',')
        .map(|i| i.trim().parse().unwrap())
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

fn solve(numbers: &Vec<u32>) -> (usize, usize) {
    let numbers_length = numbers.len();
    let mut previous_lists = vec![];
    let mut cycles = 0;
    let mut numbers = numbers.clone();
    loop {
        if let Some(index) = previous_lists.iter().position(|previous| previous == &numbers) {
            return (cycles, index)
        }
        cycles += 1;
        previous_lists.push(numbers.clone());
        let mut update_index = 0;
        let mut max_number = 0;
        for (index, number) in numbers.iter().enumerate() {
            if *number > max_number {
                max_number = *number;
                update_index = index
            }
        }
        numbers[update_index] = 0;
        while max_number > 0 {
            update_index = if update_index < numbers_length - 1 { update_index + 1 } else { 0 };
            numbers[update_index] += 1;
            max_number -= 1;
        }
    }
}

fn get_input(file_path: &String) -> Vec<u32> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split("\t")
        .map(|split| split.parse().unwrap())
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
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:7}", end);
}

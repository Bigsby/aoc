fn part2(seats: &Vec<u32>) -> u32 {
    let mut last_id = *seats.iter().min().unwrap();
    let mut seats = seats.clone();
    seats.sort();
    for current_id in seats {
        if current_id - last_id == 2 {
            return last_id + 1;
        }
        last_id = current_id;
    }
    panic!("Seat not found");
}

fn solve(seats: &Vec<u32>) -> (u32, u32) {
    (*seats.iter().max().unwrap(), part2(seats))
}

fn get_input(file_path: &String) -> Vec<u32> {
    let replacemennts = vec![("B", "1"), ("F", "0"), ("R", "1"), ("L", "0")];
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let binary = replacemennts
                .iter()
                .fold(String::from(line), |acc, replacement| {
                    String::from(acc.replace(replacement.0, replacement.1).clone().as_str())
                });
            u32::from_str_radix(binary.as_str(), 2).unwrap()
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
    println!("P1: {}", part1_result);
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:7}", now.elapsed().as_secs_f32());
}

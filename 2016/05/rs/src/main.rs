fn solve(door_id: &str) -> (String, String) {
    let mut index = 0;
    let prefix = (0..5).map(|_| '0').collect::<String>();
    let mut password1: Vec<char> = Vec::new();
    let mut password2 = (0..8).map(|_| '_').collect::<Vec<char>>();
    let mut missing_indexes = (0..8)
        .map(|index| index.to_string())
        .collect::<String>()
        .chars()
        .collect::<Vec<char>>();
    while !missing_indexes.is_empty() {
        let hash = format!("{:x}", md5::compute(format!("{}{}", door_id, index)));
        if hash.starts_with(&prefix) {
            let chars = hash.chars().collect::<Vec<char>>();
            if password1.len() < 8 {
                password1.push(chars[5]);
            }
            let digit_index = chars[5];
            if missing_indexes.contains(&digit_index) {
                password2[(digit_index.to_string()).parse::<usize>().unwrap()] = chars[6];
                missing_indexes = missing_indexes
                    .iter()
                    .filter(|index| **index != digit_index)
                    .map(|c| *c)
                    .collect();
            }
        }
        index += 1;
    }
    (
        password1.iter().collect::<String>(),
        password2.iter().collect::<String>(),
    )
}

fn get_input(file_path: &String) -> String {
    String::from(std::fs::read_to_string(file_path).expect("Error reading input file!").trim())
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

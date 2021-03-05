use std::collections::HashMap;

fn get_column_records(messages: &Vec<String>) -> Vec<HashMap<char, u32>> {
    let mut column_records: Vec<HashMap<char, u32>> = (0..messages.iter().next().unwrap().len())
        .into_iter()
        .map(|_| HashMap::new())
        .collect();
    for message in messages {
        for (column, c) in message.chars().enumerate() {
            *column_records[column].entry(c).or_insert(0) += 1;
        }
    }
    column_records
}

fn solve(messages: &Vec<String>) -> (String, String) {
    let column_records = get_column_records(messages);
    (
        (0..messages.iter().next().unwrap().len())
            .into_iter()
            .map(|column| {
                column_records[column]
                    .iter()
                    .max_by(|a, b| a.1.cmp(&b.1))
                    .map(|(letter, _)| letter)
                    .unwrap()
            })
            .collect::<String>(),
        (0..messages.iter().next().unwrap().len())
            .into_iter()
            .map(|column| {
                column_records[column]
                    .iter()
                    .min_by(|a, b| a.1.cmp(&b.1))
                    .map(|(letter, _)| letter)
                    .unwrap()
            })
            .collect::<String>(),
    )
}

fn get_input(file_path: &String) -> Vec<String> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| String::from(line))
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

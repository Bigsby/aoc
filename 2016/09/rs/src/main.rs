use regex::Regex;

fn get_length(data: &str, recursive: bool, marker_regex: &Regex) -> usize {
    if let Some(cap) = marker_regex.captures(data) {
        let data_length = cap
            .name("length")
            .unwrap()
            .as_str()
            .parse::<usize>()
            .unwrap();
        let data = cap.name("data").unwrap().as_str();
        return cap.name("prior").unwrap().as_str().len()
            + cap
                .name("repeats")
                .unwrap()
                .as_str()
                .parse::<usize>()
                .unwrap()
                * (if recursive {
                    get_length(&data[..data_length], recursive, marker_regex)
                } else {
                    data_length
                })
            + get_length(&data[data_length..], recursive, marker_regex);
    } else {
        data.len()
    }
}

fn solve(data: &str) -> (usize, usize) {
    let marker_regex =
        Regex::new(r"(?P<prior>[A-Z]*)\((?P<length>\d+)x(?P<repeats>\d+)\)(?P<data>.*)").unwrap();
    (
        get_length(data, false, &marker_regex),
        get_length(data, true, &marker_regex),
    )
}

fn get_input(file_path: &String) -> String {
    String::from(std::fs::read_to_string(file_path).expect("Error reading input file!"))
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

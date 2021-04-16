fn _print_cups(cups: &Vec<usize>, current: usize) {
    let mut current = current;
    for _ in 0..cups.len() {
        print!("{} ", current + 1);
        current = cups[current % cups.len()];
    }
    println!();
}

fn build_linked_list(cups: &Vec<usize>) -> (usize, Vec<usize>) {
    let mut result = vec![0; cups.len()];
    for index in 0..cups.len() {
        // set each index to its next
        result[cups[index]] = cups[(index + 1) % cups.len()]
    }
    (cups[0], result)
}

fn play_game(cups: &Vec<usize>, moves: usize) -> (usize, Vec<usize>) {
    let (mut current, mut cups) = build_linked_list(cups);
    for _ in 0..moves {
        let first_removed = cups[current];
        let middle_removed = cups[first_removed];
        let last_removed = cups[middle_removed];
        let mut insert_after = current;
        while insert_after == first_removed
            || insert_after == middle_removed
            || insert_after == last_removed
            || insert_after == current
        {
            insert_after = if insert_after == 0 {
                cups.len() - 1
            } else {
                insert_after - 1
            };
        }
        cups[current] = cups[last_removed];
        cups[last_removed] = cups[insert_after];
        cups[insert_after] = first_removed;
        current = cups[current];
    }
    (cups[0], cups)
}

fn part1(cups: &Vec<usize>) -> String {
    let (mut current, cups) = play_game(cups, 100);
    let mut result = Vec::new();
    for _ in 0..cups.len() - 1 {
        result.push((current + 1).to_string());
        current = cups[current % cups.len()];
    }
    result.join("")
}

fn part2(cups: &Vec<usize>) -> usize {
    let mut cups = cups.clone();
    for cup in 9..1_000_000 {
        cups.push(cup);
    }
    let (current, cups) = play_game(&cups, 10_000_000);
    (current + 1) * (cups[current % cups.len()] + 1)
}

fn solve(cups: &Vec<usize>) -> (String, usize) {
    (part1(&cups), part2(&cups))
}

fn get_input(file_path: &String) -> Vec<usize> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .trim()
        .chars()
        .map(|c| c as usize - 49) // ASCII '0' - 1 to get indexes
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

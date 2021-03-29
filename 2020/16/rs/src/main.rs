use regex::Regex;
use std::collections::HashSet;

type Ticket = Vec<u64>;
type Rule = (String, u64, u64, u64, u64);

fn get_valid_numbers(rules: &Vec<Rule>) -> HashSet<u64> {
    let mut valid_numbers = HashSet::new();
    for (_, start_one, end_one, start_two, end_two) in rules {
        for number in *start_one..*end_one + 1 {
            valid_numbers.insert(number);
        }
        for number in *start_two..*end_two + 1 {
            valid_numbers.insert(number);
        }
    }
    valid_numbers
}

fn part1(tickets: &Vec<Ticket>, valid_numbers: &HashSet<u64>) -> u64 {
    let mut total = 0;
    for ticket in tickets {
        for number in ticket {
            if !valid_numbers.contains(number) {
                total += *number;
            }
        }
    }
    total
}

fn part2(
    rules: &Vec<Rule>,
    my_ticket: &Ticket,
    tickets: &Vec<Ticket>,
    valid_numbers: &HashSet<u64>,
) -> u64 {
    let valid_tickets: Vec<Ticket> = tickets
        .into_iter()
        .filter(|ticket| ticket.iter().all(|number| valid_numbers.contains(number)))
        .map(|ticket| ticket.clone())
        .collect();
    let mut positions = Vec::new();
    let mut names = Vec::new();
    let mut ranges = Vec::new();
    let rule_count = rules.len();
    for (name, start_one, end_one, start_two, end_two) in rules.into_iter() {
        ranges.push((start_one, end_one, start_two, end_two));
        positions.push((0..rule_count).collect::<HashSet<usize>>());
        names.push(String::from(name));
    }
    for ticket in valid_tickets {
        for (ticket_index, number) in ticket.into_iter().enumerate() {
            for field_index in 0..names.len() {
                if !positions[field_index].contains(&ticket_index) {
                    continue;
                }
                let (start_one, end_one, start_two, end_two) = ranges[field_index];
                if number < *start_one
                    || (number > *end_one && number < *start_two)
                    || number > *end_two
                {
                    let mut to_remove = Vec::new();
                    positions[field_index].remove(&ticket_index);
                    if positions[field_index].len() == 1 {
                        to_remove
                            .push((field_index, *positions[field_index].iter().next().unwrap()));
                    }
                    while let Some((owner_index, position_to_remove)) = to_remove.pop() {
                        for other_field_index in 0..names.len() {
                            if other_field_index != owner_index
                                && positions[other_field_index].remove(&position_to_remove)
                            {
                                if positions[other_field_index].len() == 1 {
                                    to_remove.push((
                                        other_field_index,
                                        *positions[other_field_index].iter().next().unwrap(),
                                    ));
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    let departure_field_indexes: Vec<usize> = names
        .into_iter()
        .enumerate()
        .filter(|(_, name)| name.starts_with("departure"))
        .map(|(index, _)| *positions.get(index).unwrap().iter().next().unwrap())
        .collect();
    departure_field_indexes
        .into_iter()
        .fold(1, |acc, index| acc * my_ticket[index])
}

fn solve(puzzle_input: &(Vec<Rule>, Ticket, Vec<Ticket>)) -> (u64, u64) {
    let (rules, my_ticket, tickets) = puzzle_input;
    let valid_numbers = get_valid_numbers(rules);
    (
        part1(tickets, &valid_numbers),
        part2(rules, my_ticket, tickets, &valid_numbers),
    )
}

fn get_input(file_path: &String) -> (Vec<Rule>, Ticket, Vec<Ticket>) {
    let field_regex = Regex::new(
        r"^(?P<field>[^:]+):\s(?P<r1s>\d+)-(?P<r1e>\d+)\sor\s(?P<r2s>\d+)-(?P<r2e>\d+)$",
    )
    .unwrap();
    let ticket_regex = Regex::new(r"^(?:\d+,)+(?:\d+$)").unwrap();
    let mut rules = Vec::new();
    let mut my_ticket = Ticket::new();
    let mut tickets = Vec::new();
    let mut doing_rules = true;
    let mut doing_my_ticket = true;
    for line in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
    {
        if doing_rules {
            if let Some(cap) = field_regex.captures(line) {
                rules.push((
                    String::from(cap.name("field").unwrap().as_str()),
                    cap.name("r1s").unwrap().as_str().parse().unwrap(),
                    cap.name("r1e").unwrap().as_str().parse().unwrap(),
                    cap.name("r2s").unwrap().as_str().parse().unwrap(),
                    cap.name("r2e").unwrap().as_str().parse().unwrap(),
                ));
            } else {
                doing_rules = false;
            }
        } else if ticket_regex.is_match(line) {
            let ticket: Ticket = line.split(",").map(|v| v.trim().parse().unwrap()).collect();
            if doing_my_ticket {
                my_ticket = ticket;
                doing_my_ticket = false;
            } else {
                tickets.push(ticket);
            }
        }
    }

    (rules, my_ticket, tickets)
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

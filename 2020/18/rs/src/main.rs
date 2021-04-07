use regex::Regex;

struct Evaluator {
    paren_regex: Regex,
    plus_regex: Regex,
}

impl Evaluator {
    fn new() -> Evaluator {
        Evaluator {
            paren_regex: Regex::new(r"\((?P<expression>[^()]+)\)").unwrap(),
            plus_regex: Regex::new(r"(?P<first>\d+)\s\+\s(?P<second>\d+)").unwrap(),
        }
    }

    fn get_next_token(expression: &str) -> (String, String) {
        let mut current_token = String::default();
        for (index, c) in expression.chars().enumerate() {
            if c == ' ' {
                return (current_token, String::from(expression[index + 1..].trim()));
            }
            if current_token.parse::<u64>().is_ok() && !c.is_digit(10) {
                return (current_token, String::from(expression[index..].trim()));
            }
            current_token.push(c);
        }
        (current_token, String::default())
    }

    fn perform_operation(first: u64, operation: char, second: u64) -> u64 {
        match operation {
            '*' => first * second,
            '+' => first + second,
            _ => {
                panic!("Uknown operation '{}'", operation);
            }
        }
    }

    fn evaluate_expression(&self, expression: &str, add_first: bool) -> u64 {
        let mut expression = String::from(expression);
        while let Some(paren_match) = self.paren_regex.captures(expression.as_str()) {
            let mut new_expression = String::default();
            new_expression.push_str(&expression[..paren_match.get(0).unwrap().start()]);
            new_expression.push_str(
                &self
                    .evaluate_expression(
                        paren_match.name("expression").unwrap().as_str(),
                        add_first,
                    )
                    .to_string(),
            );
            new_expression.push_str(&expression[paren_match.get(0).unwrap().end()..]);
            expression = new_expression;
        }
        if add_first {
            while let Some(plus_match) = self.plus_regex.captures(expression.as_str()) {
                let mut new_expression = String::default();
                new_expression.push_str(&expression[..plus_match.get(0).unwrap().start()]);
                let first = plus_match
                    .name("first")
                    .unwrap()
                    .as_str()
                    .parse::<u32>()
                    .unwrap();
                let second = plus_match
                    .name("second")
                    .unwrap()
                    .as_str()
                    .parse::<u32>()
                    .unwrap();
                new_expression.push_str((first + second).to_string().as_str());
                new_expression.push_str(&expression[plus_match.get(0).unwrap().end()..]);
                expression = new_expression;
            }
        }
        let (token, expression) = Evaluator::get_next_token(&expression);
        let mut expression = expression;
        let mut current_value = token.parse::<u64>().unwrap();
        let mut operation_to_perform = '\0';
        while !expression.is_empty() {
            let (token, new_expression) = Evaluator::get_next_token(&expression);
            if let Ok(value) = token.parse() {
                current_value =
                    Evaluator::perform_operation(current_value, operation_to_perform, value)
            } else {
                operation_to_perform = token.chars().next().unwrap();
            }
            expression = new_expression;
        }
        current_value
    }

    fn evaluate_expressions(&self, add_first: bool, expressions: &Vec<String>) -> u64 {
        expressions
            .into_iter()
            .map(|expression| self.evaluate_expression(expression, add_first))
            .sum()
    }
}

fn solve(expressions: &Vec<String>) -> (u64, u64) {
    let evaluator = Evaluator::new();
    (
        evaluator.evaluate_expressions(false, expressions),
        evaluator.evaluate_expressions(true, expressions),
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
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}

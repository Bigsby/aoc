pub struct PasswordCalculator {
    forbiden_letters: Vec<u8>,
    a_char: u8,
    z_ord: u8,
}

impl PasswordCalculator {
    pub fn new() -> PasswordCalculator {
        PasswordCalculator {
            forbiden_letters: vec![b'i', b'o', b'l'],
            a_char: b'a',
            z_ord: b'z',
        }
    }

    pub fn calculate_next_valid_password(&self, current_password: &str) -> String {
        let mut next_password =
            self.calculate_next_password(current_password.chars().map(|c| c as u8).collect());
        while !self.is_password_valid(&next_password) {
            next_password = self.calculate_next_password(next_password);
        }
        next_password.into_iter().map(|c| c as char).collect()
    }

    fn calculate_next_password(&self, current_password: Vec<u8>) -> Vec<u8> {
        let mut result: Vec<u8> = current_password.clone();
        for index in (0..result.len()).rev() {
            let c_ord = result[index] as u8;
            if c_ord == self.z_ord {
                result[index] = self.a_char;
                continue;
            }
            result[index] = self.get_next_char(c_ord);
            break;
        }
        result
    }

    fn get_next_char(&self, c: u8) -> u8 {
        let mut c = c + 1;
        while self.forbiden_letters.contains(&c) {
            c += 1;
        }
        c
    }

    fn is_password_valid(&self, password: &Vec<u8>) -> bool {
        let length = password.len();
        let mut sequence_found = false;
        let mut pairs_count = 0;
        let mut skip_pair = false;
        for index in 0..length - 1 {
            if skip_pair {
                skip_pair = false;
            } else {
                if password[index] == password[index + 1] {
                    pairs_count += 1;
                    skip_pair = true;
                } else {
                    skip_pair = false;
                }
            }
            if !sequence_found && index < length - 2 {
                sequence_found = password[index] == password[index + 1] - 1
                    && password[index] == password[index + 2] - 2;
            }
        }
        return sequence_found && pairs_count > 1;
    }
}

fn solve(current_password: &str) -> (String, String) {
    let password_calculator = PasswordCalculator::new();
    let next_password = &password_calculator.calculate_next_valid_password(current_password);
    let part1 = next_password.clone();
    (
        part1,
        password_calculator.calculate_next_valid_password(next_password),
    )
}

fn get_input(file_path: &String) -> String {
    String::from(
        std::fs::read_to_string(file_path)
            .expect("Error reading input file!")
            .trim(),
    )
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

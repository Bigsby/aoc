struct PowerIterator {
    limits: [u64; 6],
    powers: [u64; 6],
    done: bool,
}

impl PowerIterator {
    fn new(limits: [u64; 6]) -> PowerIterator {
        PowerIterator {
            limits,
            powers: [0; 6],
            done: false,
        }
    }
}

impl Iterator for PowerIterator {
    type Item = [u64; 6];
    fn next(&mut self) -> Option<<Self as Iterator>::Item> {
        if self.done {
            return None;
        }
        let mut all_equal = true;
        for index in 0..6 {
            all_equal &= self.powers[index] == self.limits[index];
        }
        self.done = all_equal;
        let return_powers = Some(self.powers);
        for index in (0..6).rev() {
            if self.powers[index] < self.limits[index] {
                self.powers[index] += 1;
                for overflow in index + 1..6 {
                    self.powers[overflow] = 0;
                }
                break;
            }
        }
        return return_powers;
    }
}

static DIVISORS: [u64; 6] = [2, 3, 5, 7, 11, 13];
fn calculate_powers(powers: [u64; 6]) -> u64 {
    powers
        .iter()
        .zip(DIVISORS.iter())
        .fold(1, |acc, (j, k)| acc * (k.pow(*j as u32)))
}

static MAX_POWERS: [u64; 6] = [6, 4, 2, 2, 2, 2];
fn get_house(target: u64, multiplier: u64, limit: u64) -> u64 {
    let mut minimum_house = u64::MAX;
    for house_powers in PowerIterator::new(MAX_POWERS) {
        let house = calculate_powers(house_powers);
        let mut house_presents = 0;
        for elf_powers in PowerIterator::new(house_powers) {
            let elf_presents = calculate_powers(elf_powers);
            if house / elf_presents <= limit {
                house_presents += elf_presents;
            }
        }
        if house_presents * multiplier >= target && house < minimum_house {
            minimum_house = house;
        }
    }
    minimum_house
}

fn solve(puzzle_input: &u64) -> (u64, u64) {
    (
        get_house(*puzzle_input, 10, u64::MAX),
        get_house(*puzzle_input, 11, 50),
    )
}

fn get_input(file_path: &String) -> u64 {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .trim()
        .parse()
        .unwrap()
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

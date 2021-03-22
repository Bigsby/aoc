const MODULUS: u64 = 2147483647;

struct Generator {
    number: u64,
    factor: u64,
    divisor: u64,
}

impl Generator {
    fn new(number: u64, factor: u64, divisor: u64) -> Generator {
        Generator {
            number,
            factor,
            divisor,
        }
    }
}

impl Iterator for Generator {
    type Item = u64;
    fn next(&mut self) -> Option<<Self as std::iter::Iterator>::Item> {
        loop {
            self.number = self.number * self.factor % MODULUS;
            if self.number % self.divisor == 0 {
                return Some(self.number & 0xffff);
            }
        }
    }
}

const FACTOR_A: u64 = 16807;
const FACTOR_B: u64 = 48271;
fn run_sequences(
    generators: &(u64, u64),
    divisor_a: u64,
    divisor_b: u64,
    million_cycles: u32,
) -> usize {
    let (generator_a, generator_b) = generators;
    let mut sequence_a = Generator::new(*generator_a, FACTOR_A, divisor_a);
    let mut sequence_b = Generator::new(*generator_b, FACTOR_B, divisor_b);
    (0..million_cycles * u32::pow(10, 6))
        .filter(|_| sequence_a.next() == sequence_b.next())
        .count()
}

const DIVISOR_A: u64 = 4;
const DIVISOR_B: u64 = 8;
fn solve(generators: &(u64, u64)) -> (usize, usize) {
    (
        run_sequences(generators, 1, 1, 40),
        run_sequences(generators, DIVISOR_A, DIVISOR_B, 5),
    )
}

fn get_input(file_path: &String) -> (u64, u64) {
    let lines: Vec<String> = std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| String::from(line))
        .collect();
    (
        lines[0].split(" ").last().unwrap().trim().parse().unwrap(),
        lines[1].split(" ").last().unwrap().trim().parse().unwrap(),
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

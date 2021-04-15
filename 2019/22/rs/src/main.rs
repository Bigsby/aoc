type Unit = i128;
#[derive(Debug, Clone, Copy)]
enum Shuffle {
    Deal,
    Cut(Unit),
    Increment(Unit),
}

fn _pause() {
    std::io::stdin().read_line(&mut String::new()).expect("");
}

const CARDS1: Unit = 10007;
const POSITION1: Unit = 2019;

fn part1(shuffles: &Vec<Shuffle>) -> Unit {
    let mut position = POSITION1;
    for shuffle in shuffles {
        position = match *shuffle {
            Shuffle::Deal => CARDS1 - 1 - position,
            Shuffle::Cut(count) => (position - count + CARDS1) % CARDS1,
            Shuffle::Increment(count) => count * position % CARDS1,
        };
    }
    position
}

fn inverse_modulo(mut a: i128, mut base: i128) -> i128 {
    if base == 1 {
        return 0;
    }
    let orig = base;
    let mut x = 1;
    let mut y = 0;
    while a > 1 {
        let q = a / base;
        let tmp = base;
        base = a % base;
        a = tmp;
        let tmp = y;
        y = x - q * y;
        x = tmp;
    }
    if x < 0 {
        x + orig
    } else {
        x
    }
}

fn mod_pow(base: i128, exp: i128, modulo: i128) -> i128 {
    let mut x = 1;
    let mut p = base % modulo;
    for i in 0..128 {
        if 1 & (exp >> i) == 1 {
            x = x * p % modulo;
        }
        p = p * p % modulo;
    }
    x
}

const CARDS2: Unit = 119315717514047;
const RUNS: Unit = 101741582076661;
const POSITION2: Unit = 2020;

fn part2(shuffles: &Vec<Shuffle>) -> Unit {
    let mut a = 1;
    let mut b = 0;
    for &shuffle in shuffles.iter().rev() {
        match shuffle {
            Shuffle::Deal => {
                b += 1;
                b *= -1;
                a *= -1;
            }
            Shuffle::Cut(count) => {
                b += if count < 0 { count + CARDS2 } else { count };
            }
            Shuffle::Increment(count) => {
                let inv = inverse_modulo(count, CARDS2);
                a = a * inv % CARDS2;
                b = b * inv % CARDS2;
            }
        }
        a %= CARDS2;
        b %= CARDS2;
        if a < 0 {
            a += CARDS2;
        }
        if b < 0 {
            b += CARDS2;
        }
    }
    let i1 = mod_pow(a, RUNS, CARDS2) * POSITION2 % CARDS2;
    let i2 = (mod_pow(a, RUNS, CARDS2) + CARDS2 - 1) % CARDS2;
    let i3 = b * i2 % CARDS2;
    let i4 = mod_pow(a - 1, CARDS2 - 2, CARDS2);
    (i1 + i3 * i4) % CARDS2
}

fn solve(shuffles: &Vec<Shuffle>) -> (Unit, Unit) {
    (part1(shuffles), part2(shuffles))
}

fn get_input(file_path: &String) -> Vec<Shuffle> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let splits: Vec<&str> = line.split(" ").collect();
            if line.starts_with("deal into") {
                Shuffle::Deal
            } else if line.starts_with("cut") {
                Shuffle::Cut(splits[1].parse().unwrap())
            } else if line.starts_with("deal with") {
                Shuffle::Increment(splits[3].parse().unwrap())
            } else {
                panic!("Unknow shuffle '{}'", line);
            }
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
    let end = now.elapsed().as_secs_f32();
    println!("P1: {}", part1_result);
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}

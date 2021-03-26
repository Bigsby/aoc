use regex::Regex;

const PROPS: &'static [&'static str] = &[
    "children",
    "cats",
    "samoyeds",
    "pomeranians",
    "akitas",
    "vizslas",
    "goldfish",
    "trees",
    "cars",
    "perfumes",
];

static MFCSAN_READING: &'static [Reading] = &[
    Reading::Equal(3),   // children
    Reading::Greater(7), // cats
    Reading::Equal(2),   // samoyeds
    Reading::Less(3),    // pomeranians
    Reading::Equal(0),   // akitas
    Reading::Equal(0),   // vizslas
    Reading::Less(5),    // goldfish
    Reading::Greater(3), // trees
    Reading::Equal(2),   // cars
    Reading::Equal(1),   // perfumes
];

fn prop_index(name: &str) -> usize {
    PROPS.iter().position(|n| *n == name).unwrap()
}

#[derive(Debug)]
struct AuntRecord {
    number: u32,
    props: Vec<Option<i32>>,
}

impl AuntRecord {
    fn new(
        number: u32,
        prop1_name: &str,
        prop1_value: i32,
        prop2_name: &str,
        prop2_value: i32,
        prop3_name: &str,
        prop3_value: i32,
    ) -> AuntRecord {
        let mut props = vec![None; PROPS.len()];
        props[prop_index(prop1_name)] = Some(prop1_value);
        props[prop_index(prop2_name)] = Some(prop2_value);
        props[prop_index(prop3_name)] = Some(prop3_value);
        AuntRecord { number, props }
    }

    fn get_value(&self, prop: &usize) -> Option<i32> {
        self.props[*prop]
    }
}

enum Reading {
    Equal(i32),
    Greater(i32),
    Less(i32),
}

impl Reading {
    fn is_valid(&self, value: &i32) -> bool {
        match self {
            Reading::Equal(check) => value == check,
            Reading::Greater(check) => value > check,
            Reading::Less(check) => value < check,
        }
    }

    fn get_value(&self) -> i32 {
        match self {
            Reading::Equal(check) => *check,
            Reading::Greater(check) => *check,
            Reading::Less(check) => *check,
        }
    }
}

fn is_valid_record(record: &AuntRecord, check_operator: bool) -> bool {
    for (prop, reading) in MFCSAN_READING.iter().enumerate() {
        if let Some(record_value) = record.get_value(&prop) {
            if check_operator {
                if !reading.is_valid(&record_value) {
                    return false;
                }
            } else if record_value != reading.get_value() {
                return false;
            }
        }
    }
    true
}

fn solve(aunts: &Vec<AuntRecord>) -> (u32, u32) {
    (
        aunts
            .iter()
            .filter(|record| is_valid_record(*record, false))
            .next()
            .unwrap()
            .number,
        aunts
            .iter()
            .filter(|record| is_valid_record(*record, true))
            .next()
            .unwrap()
            .number,
    )
}

fn get_input(file_path: &String) -> Vec<AuntRecord> {
    let line_regex =
        Regex::new(r"^Sue\s(\d+):\s(\w+):\s(\d+),\s(\w+):\s(\d+),\s(\w+):\s(\d+)$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            line_regex
                .captures(line)
                .map(|cap| {
                    AuntRecord::new(
                        cap.get(1).unwrap().as_str().parse().unwrap(),
                        cap.get(2).unwrap().as_str(),
                        cap.get(3).unwrap().as_str().parse().unwrap(),
                        cap.get(4).unwrap().as_str(),
                        cap.get(5).unwrap().as_str().parse().unwrap(),
                        cap.get(6).unwrap().as_str(),
                        cap.get(7).unwrap().as_str().parse().unwrap(),
                    )
                })
                .unwrap()
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

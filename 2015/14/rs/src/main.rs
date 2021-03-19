use regex::Regex;

const TIME: u32 = 2503;

#[derive(Debug, Clone, Copy)]
struct Entry {
    speed: u32,
    duration: u32,
    rest: u32,
    period: u32,
}

impl Entry {
    fn new(speed: u32, duration: u32, rest: u32) -> Entry {
        Entry {
            speed,
            duration,
            rest,
            period: duration + rest,
        }
    }

    fn calculate_distance(&self, total_duration: u32) -> u32 {
        let (periods, remainder) = (total_duration / self.period, total_duration % self.period);
        let total = periods * self.speed * self.duration;
        total + self.speed * remainder.min(self.duration)
    }

    fn get_distance_for_time(&self, time: u32) -> u32 {
        if time % self.period < self.duration {
            self.speed
        } else {
            0
        }
    }
}

struct Deer {
    entry: Entry,
    distance: u32,
    points: u32,
}

impl Deer {
    fn new(entry: Entry) -> Deer {
        Deer {
            entry,
            distance: 0,
            points: 0,
        }
    }
}

fn part2(entries: &Vec<Entry>) -> u32 {
    let mut deers: Vec<Deer> = entries.into_iter().map(|entry| Deer::new(*entry)).collect();
    for time in 0..TIME {
        let mut max_distance = 0;
        for deer in deers.iter_mut() {
            deer.distance += deer.entry.get_distance_for_time(time);
            max_distance = max_distance.max(deer.distance);
        }
        for deer in deers.iter_mut() {
            if deer.distance == max_distance {
                deer.points += 1;
            }
        }
    }
    deers.into_iter().map(|deer| deer.points).max().unwrap()
}

fn solve(entries: &Vec<Entry>) -> (u32, u32) {
    (
        entries
            .iter()
            .map(|entry| entry.calculate_distance(TIME))
            .max()
            .unwrap(),
        part2(entries),
    )
}

fn get_input(file_path: &String) -> Vec<Entry> {
    let line_regex = Regex::new(r"^\w+\scan\sfly\s(\d+)\skm/s\sfor\s(\d+)\sseconds,\sbut\sthen\smust\srest\sfor\s(\d+)\sseconds.$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            line_regex
                .captures(line)
                .map(|cap| {
                    Entry::new(
                        cap.get(1).unwrap().as_str().parse().unwrap(),
                        cap.get(2).unwrap().as_str().parse().unwrap(),
                        cap.get(3).unwrap().as_str().parse().unwrap(),
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

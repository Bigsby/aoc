use itertools::Itertools;
use regex::RegexBuilder;

type Player = (i32, i32, i32);

static WEAPONS: &'static [(i32, i32, i32)] =
    &[(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)];
static ARMORS: &'static [(i32, i32, i32)] = &[
    (0, 0, 0),
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
];
static RINGS: &'static [(i32, i32, i32)] = &[
    (0, 0, 0),
    (0, 0, 0),
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
];

fn play_game(player: &Player, boss: &Player) -> bool {
    let (mut player_hit, player_damage, player_armor) = player;
    let (mut boss_hit, boss_damage, boss_armor) = boss;
    let player_damage = 1.max(player_damage - boss_armor);
    let boss_damage = 1.max(boss_damage - player_armor);
    loop {
        boss_hit -= player_damage;
        if boss_hit <= 0 {
            return true;
        }
        player_hit -= boss_damage;
        if player_hit <= 0 {
            return false;
        }
    }
}

fn get_inventory_combinations() -> Vec<(i32, i32, i32)> {
    let mut combinations = Vec::new();
    for weapon in WEAPONS {
        for armor in ARMORS {
            for rings in RINGS.iter().combinations(2) {
                let inventory = [weapon, armor, rings[0], rings[1]];
                combinations.push(inventory.iter().fold((0, 0, 0), |acc, item| {
                    (acc.0 + item.0, acc.1 + item.1, acc.2 + item.2)
                }));
            }
        }
    }
    combinations
}

fn solve(boss: &Player) -> (i32, i32) {
    let mut min_cost = i32::MAX;
    let mut max_cost = 0;
    for (cost, damage, defense) in get_inventory_combinations() {
        if play_game(&(100, damage, defense), boss) {
            min_cost = min_cost.min(cost);
        } else {
            max_cost = max_cost.max(cost);
        }
    }
    (min_cost, max_cost)
}

fn get_input(file_path: &String) -> Player {
    let input_regex = RegexBuilder::new(
        r"^Hit Points: (?P<hit>\d+)\W+Damage: (?P<damage>\d+)\W+^Armor: (?P<armor>\d+)",
    )
    .multi_line(true)
    .build()
    .unwrap();
    input_regex
        .captures(&std::fs::read_to_string(file_path).expect("Error reading input file!"))
        .map(|cap| {
            (
                cap.name("hit").unwrap().as_str().parse().unwrap(),
                cap.name("damage").unwrap().as_str().parse().unwrap(),
                cap.name("armor").unwrap().as_str().parse().unwrap(),
            )
        })
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

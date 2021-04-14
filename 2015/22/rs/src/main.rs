use std::collections::VecDeque;

type Spell = (i32, i32, i32, i32, i32, i32);

static SPELLS: &'static [Spell] = &[
    // cost, damage, hitPoints, armor, mana, duration
    (53, 4, 0, 0, 0, 0),    // Magic Missile
    (73, 2, 2, 0, 0, 0),    // Drain
    (113, 0, 0, 7, 0, 6),   // Shield
    (173, 3, 0, 0, 0, 6),   // Poison
    (229, 0, 0, 0, 101, 5), // Recharge
];

fn get_least_winning_mana(data: &(i32, i32), lose_hit_on_player_turn: bool) -> i32 {
    let (boss_hit, boss_damage) = data;
    let mut least_mana_spent = i32::MAX;
    let mut queue: VecDeque<(i32, i32, i32, Vec<Spell>, bool, i32)> = VecDeque::new();
    queue.push_back((*boss_hit, 50, 500, vec![], true, 0));
    while let Some((
        mut boss_hit,
        player_hit,
        mut player_mana,
        active_spells,
        player_turn,
        mana_spent,
    )) = queue.pop_back()
    {
        let mut player_hit = player_hit;
        if lose_hit_on_player_turn && player_turn {
            player_hit -= 1;
            if player_hit <= 0 {
                continue;
            }
        }
        let mut player_armor = 0;
        let mut updated_spells = Vec::new();
        for active_spell in active_spells {
            let (cost, damage, hit_points, armor, mana, duration) = active_spell;
            if duration >= 0 {
                boss_hit -= damage;
                player_hit += hit_points;
                player_armor += armor;
                player_mana += mana;
            }
            if duration > 1 {
                updated_spells.push((cost, damage, hit_points, armor, mana, duration - 1));
            }
        }
        if boss_hit <= 0 {
            least_mana_spent = least_mana_spent.min(mana_spent);
            continue;
        }
        if mana_spent > least_mana_spent {
            continue;
        }
        if player_turn {
            let active_costs: Vec<i32> = updated_spells.iter().map(|spell| spell.0).collect();
            for spell in SPELLS {
                let spell_cost = spell.0;
                // cost is unique per spell
                if !active_costs.contains(&spell_cost) && spell_cost <= player_mana {
                    let mut new_active_spells = updated_spells.clone();
                    new_active_spells.push(spell.clone());
                    queue.push_back((
                        boss_hit,
                        player_hit,
                        player_mana - spell_cost,
                        new_active_spells,
                        false,
                        mana_spent + spell_cost,
                    ));
                }
            }
        } else {
            player_hit -= 1.max(boss_damage - player_armor);
            if player_hit > 0 {
                queue.push_back((
                    boss_hit,
                    player_hit,
                    player_mana,
                    updated_spells,
                    true,
                    mana_spent,
                ))
            }
        }
    }
    least_mana_spent
}

fn solve(data: &(i32, i32)) -> (i32, i32) {
    (
        get_least_winning_mana(data, false),
        get_least_winning_mana(data, true),
    )
}

fn get_input(file_path: &String) -> (i32, i32) {
    let lines = std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|s| String::from(s))
        .collect::<Vec<String>>();
    (
        lines[0]
            .split(" ")
            .collect::<Vec<&str>>()
            .last()
            .unwrap()
            .parse()
            .unwrap(),
        lines[1]
            .split(" ")
            .collect::<Vec<&str>>()
            .last()
            .unwrap()
            .parse()
            .unwrap(),
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

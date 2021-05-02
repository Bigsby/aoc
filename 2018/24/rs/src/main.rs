use regex::Regex;
use std::collections::HashMap;

type Unit = i32;

#[derive(Clone, Copy)]
struct Group {
    id: (Unit, Unit),
    units: Unit,
    hit_points: Unit,
    immunities: usize,
    weaknesses: usize,
    initiative: Unit,
    type_: usize,
    damage: Unit,
    army: Unit,
    target_id: Option<(Unit, Unit)>,
}

impl Group {
    fn new(
        id: (Unit, Unit),
        units: Unit,
        hit_points: Unit,
        immunities: usize,
        weaknesses: usize,
        initiative: Unit,
        type_: usize,
        damage: Unit,
        army: Unit,
    ) -> Group {
        Group {
            id,
            units,
            hit_points,
            immunities,
            weaknesses,
            initiative,
            type_,
            damage,
            army,
            target_id: None,
        }
    }

    fn effective_power(&self) -> Unit {
        self.units * self.damage
    }

    fn has_immunity(&self, immunity: usize) -> bool {
        self.immunities & immunity == immunity
    }

    fn has_weakness(&self, weakness: usize) -> bool {
        self.weaknesses & weakness == weakness
    }

    fn damage_to(&self, target: &Self) -> Unit {
        if target.has_immunity(self.type_) {
            0
        } else {
            self.effective_power()
                * (if target.has_weakness(self.type_) {
                    2
                } else {
                    1
                })
        }
    }

    fn attack(&mut self, killed: Unit) {
        self.units -= killed;
    }

    fn clone(&self, boost: Unit) -> Group {
        Group {
            id: self.id,
            units: self.units,
            hit_points: self.hit_points,
            immunities: self.immunities.clone(),
            weaknesses: self.weaknesses.clone(),
            initiative: self.initiative,
            type_: self.type_.clone(),
            damage: self.damage + boost,
            army: self.army,
            target_id: None,
        }
    }
}

fn _pause() {
    std::io::stdin()
        .read_line(&mut String::new())
        .expect("error inputing");
}

fn combat(groups: &Vec<Group>, boost: Unit) -> (Unit, Unit) {
    let mut groups: Vec<Group> = groups
        .iter()
        .map(|group| group.clone(if group.army == 0 { boost } else { 0 }))
        .collect();
    loop {
        groups.sort_by_key(|group| (-group.effective_power(), -group.initiative));
        let mut selected_targets = HashMap::new();
        for (index, group) in groups.iter().enumerate() {
            let mut targets: Vec<Group> = groups
                .iter()
                .filter(|target| {
                    target.army != group.army
                        && !selected_targets.contains_key(&target.id)
                        && group.damage_to(target) > 0
                })
                .copied()
                .collect();
            if !targets.is_empty() {
                targets.sort_by_key(|target| {
                    (
                        -group.damage_to(target),
                        -target.effective_power(),
                        -target.initiative,
                    )
                });
                selected_targets.insert(
                    targets.iter().map(|target| target.id).next().unwrap(),
                    index,
                );
            }
        }
        let mut units_killed = false;
        for (target_id, index) in selected_targets {
            groups[index].target_id = Some(target_id);
        }
        let mut attacks = Vec::new();
        groups.sort_by_key(|group| -group.initiative);
        for (attacker_index, group) in groups.iter().enumerate() {
            if let Some(target_id) = group.target_id {
                let target = groups
                    .iter()
                    .enumerate()
                    .filter(|g| g.1.id == target_id)
                    .next()
                    .unwrap();
                attacks.push((attacker_index, target.0));
            }
        }
        for (attacker_index, target_index) in attacks {
            let killed = groups[target_index].units.min(
                groups[attacker_index].damage_to(&groups[target_index])
                    / groups[target_index].hit_points,
            );
            units_killed |= killed > 0;
            groups[target_index].attack(killed);
        }
        groups.retain(|group| group.units > 0);
        for group in groups.iter_mut() {
            group.target_id = None;
        }
        let immune_system_units = groups
            .iter()
            .filter_map(|g| if g.army == 0 { Some(g.units) } else { None })
            .sum::<Unit>();
        let infection_units = groups
            .iter()
            .filter_map(|g| if g.army == 1 { Some(g.units) } else { None })
            .sum::<Unit>();
        if !units_killed || immune_system_units == 0 {
            return (1, infection_units);
        }
        if infection_units == 0 {
            return (0, immune_system_units);
        }
    }
}

fn solve(groups: &Vec<Group>) -> (Unit, Unit) {
    let mut boost = 0;
    loop {
        boost += 1;
        let (winner, left) = combat(groups, boost);
        if winner == 0 {
            return (combat(groups, 0).1, left);
        }
    }
}

fn parse_group(text: &str, army: Unit, number: i32, skills: &mut HashMap<String, usize>) -> Group {
    let numbers_regex = Regex::new(r"^(?P<units>\d+) units.*with (?P<hit>\d+) hit.*does (?P<damage>\d+) (?P<type>\w+).*initiative (?P<initiative>\d+)$").unwrap();
    let immunity_weakness_regex = &Regex::new(r"\((.*)\)").unwrap();
    let get_skill = &mut |skill| {
        if !skills.contains_key(skill) {
            skills.insert(String::from(skill), 1 << skills.len());
        }
        *skills.get(skill).unwrap()
    };
    if let Some(number_cap) = numbers_regex.captures(text) {
        let mut immunities = 0;
        let mut weaknesses = 0;
        if let Some(immunity_weakness_cap) = immunity_weakness_regex.captures(text.trim()) {
            for group in immunity_weakness_cap.get(1).unwrap().as_str().split(';') {
                if group.trim().starts_with("weak") {
                    weaknesses = group[8..]
                        .split(",")
                        .fold(0, |acc, w| acc | get_skill(w.trim()));
                } else if group.trim().starts_with("immune") {
                    immunities = group[10..]
                        .split(",")
                        .fold(0, |acc, w| acc | get_skill(w.trim()));
                }
            }
        }
        return Group::new(
            (army, number),
            number_cap.name("units").unwrap().as_str().parse().unwrap(),
            number_cap.name("hit").unwrap().as_str().parse().unwrap(),
            immunities,
            weaknesses,
            number_cap
                .name("initiative")
                .unwrap()
                .as_str()
                .parse()
                .unwrap(),
            get_skill(number_cap.name("type").unwrap().as_str()),
            number_cap.name("damage").unwrap().as_str().parse().unwrap(),
            army,
        );
    } else {
        panic!("Bad format for group '{}'", text)
    }
}

fn parse_army(text: &str, army: Unit, skills: &mut HashMap<String, usize>) -> Vec<Group> {
    let split: Vec<&str> = text.split("\n").skip(1).collect();
    let mut groups = Vec::new();
    for (index, group_text) in split.iter().enumerate() {
        if !group_text.is_empty() {
            groups.push(parse_group(group_text, army, index as Unit + 1, skills));
        }
    }
    groups
}

fn get_input(file_path: &String) -> Vec<Group> {
    let mut groups = Vec::new();
    let mut skills = HashMap::new();
    let army_texts: Vec<String> = std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split("\n\n")
        .map(|s| String::from(s))
        .collect();
    for immune_system in parse_army(&army_texts[0], 0, &mut skills) {
        groups.push(immune_system);
    }
    for infection in parse_army(&army_texts[1], 1, &mut skills) {
        groups.push(infection);
    }
    // println!("{:?}", skills);
    groups
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

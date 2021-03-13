for year in {2015..2020}
do
    for day in {1..25}
        do
            curl https://adventofcode.com/$year/day/$day/input --cookie "session=$SESSION" -o "$year-`printf %02d $day`.txt"
        done
done

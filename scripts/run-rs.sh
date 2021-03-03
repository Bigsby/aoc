for year in {2015..2020}
do
    for day in {1..25}
    do
        echo "$year/`printf %02d $day` cs"
        { time cargo run --quiet --manifest-path ../$year/`printf %02d $day`/rs/Cargo.toml "../$year/`printf %02d $day`/input.txt" ; } 2>&1
        echo "---------------------------------------"
    done
done

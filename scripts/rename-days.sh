for year in {2015..2020}
do
    for day in {1..25}
    do
        git mv "../$year/day_`printf %02d $day`" "../$year/`printf %02d $day`"
    done
done

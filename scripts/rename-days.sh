for year in {2015..2020}
do
    for day in {1..25}
    do
        git rm -r "../$year/`printf %02d $day`/day_`printf %02d $day`"
    done
done

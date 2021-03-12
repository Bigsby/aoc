declare -A languages=(
    ["py"]="|py/run.py "
    ["cs"]="dotnet run -p|cs/run.csproj " 
    ["rs"]="cargo run --quiet --manifest-path|rs/Cargo.toml "
    ["cpp"]="make -f |cpp/make INPUT="
    ["js"]="node|js/run.js "
)

languages_to_run=${!languages[@]}
if [[ "$1" ]] ; then 
    if [[ -v "languages[$1]" ]] ; then
        languages_to_run=($1)
    else
        echo "Language not found. Options are: $languages_to_run"
        exit
    fi
fi

for year in {2015..2020} ; do
    for day in {1..25} ; do
        for language in $languages_to_run ; do
            IFS="|" read -r -a parts <<< ${languages[$language]}
            echo "$year/`printf %02d $day` $language"
            { time ${parts[0]} ../$year/`printf %02d $day`/${parts[1]}"../$year/`printf %02d $day`/input0.txt" ; } 2>&1
            echo "---------------------------------------"
        done
    done
done

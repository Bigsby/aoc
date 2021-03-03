param([validateset("py", "cs", "rs")][string] $lang)

$languages = @{
    "py" = @{
        "prefix" = "python";
        "sufix" = "py/run.py"
    };
    "cs" = @{
        "prefix" = "dotnet run -p";
        "sufix" = "cs/run.csproj"
    };
    "rs" = @{
        "prefix" = "cargo run --quiet --manifest-path";
        "sufix" = "rs/Cargo.toml"
    }
}

$languagesToRun = @($languages.Keys)
if ($lang) {
    $languagesToRun = @($lang)
}

foreach ($year in 2015..2016) {
    foreach ($day in 1..2) {
        $paddedDay = ([string]$day).PadLeft(2,'0')
        foreach ($language in $languagesToRun) {
            Write-Output "$year/$paddedDay $($language)"
            $sw = [Diagnostics.Stopwatch]::StartNew()
            $output = Invoke-Expression "$($languages[$language]["prefix"]) ../$year/$paddedDay/$($languages[$language]["sufix"]) ../$year/$paddedDay/input.txt"
            $sw.Stop()
            $duration = $sw.Elapsed
            Write-Output $output
            Write-Output ""
            Write-Output "time: $duration"
            Write-Output "---------------------------------------"    
        }
    }
}
foreach ($year in 2015..2020) {
    foreach ($day in 1..25) {
        $paddedDay = ([string]$day).PadLeft(2,'0')
        Write-Output "$year/day_$paddedDay cs"
        $sw = [Diagnostics.Stopwatch]::StartNew()
        $output = dotnet run -p ../$year/day_$paddedDay/cs/run.csproj ../$year/day_$paddedDay/input.txt
        $sw.Stop()
        $duration = $sw.Elapsed
        Write-Output $output
        Write-Output ""
        Write-Output "time: $duration"
        Write-Output "---------------------------------------"
    }
}
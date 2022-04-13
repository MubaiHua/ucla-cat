$dir = pwd | select -Expand Path
$full_path = Get-ChildItem -Filter main.exe -Recurse | %{$_.FullName}
$action = New-ScheduledTaskAction -Execute $full_path -WorkingDirectory $dir
$trigger = New-ScheduledTaskTrigger -Daily -At 12:01am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskPath "ucla-cat" -TaskName "auto-fill-survey" -Description "This task opens main.exe to auto fill symptom monitoring survey"

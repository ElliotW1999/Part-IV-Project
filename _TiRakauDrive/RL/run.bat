@echo off
for /F "tokens=2" %%i in ('date /t') do set startdate=%%i
set starttime=%time%
for /l %%y in (1, 1, 500) do (
    for /l %%x in (1, 1, 10) do (
        C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe RL-runner.py 0
        C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe learn.py
    )
    C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe RL-runner.py 1
    C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe calculateLossCurve.py 
)

for /F "tokens=2" %%i in ('date /t') do set enddate=%%i
set endtime=%time%
echo start time is %startdate%:%starttime%
echo end time is %enddate%:%endtime%
pause


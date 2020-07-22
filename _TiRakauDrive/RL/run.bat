@echo off
for /F "tokens=2" %%i in ('date /t') do set startdate=%%i
set starttime=%time%
for /l %%x in (1, 1, 40000) do (
    C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe RL-runner.py
    C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe learn.py
)
for /F "tokens=2" %%i in ('date /t') do set enddate=%%i
set endtime=%time%
echo start time is %startdate%:%starttime%
echo end time is %enddate%:%endtime%
pause
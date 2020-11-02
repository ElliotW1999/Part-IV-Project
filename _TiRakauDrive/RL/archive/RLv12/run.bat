@echo off
C:\Anaconda\python.exe RL-runner.py 1
C:\Anaconda\python.exe calculateLossCurve.py 
for /F "tokens=2" %%i in ('date /t') do set startdate=%%i
set starttime=%time%
for /l %%y in (1, 1, 40) do (
    for /l %%y in (1, 1, 5) do (
        for /l %%x in (1, 1, 60) do (
            C:\Anaconda\python.exe RL-runner.py 0
            C:\Anaconda\python.exe learn.py
        )
        C:\Anaconda\python.exe RL-runner.py 1
        C:\Anaconda\python.exe calculateLossCurve.py 
    )
    C:\Anaconda\python.exe RL-runner.py 1
    C:\Anaconda\python.exe learn.py
)
C:\Anaconda\python.exe analyzelosscurves.py
for /F "tokens=2" %%i in ('date /t') do set enddate=%%i
set endtime=%time%
echo start time is %startdate%:%starttime%
echo end time is %enddate%:%endtime%
pause
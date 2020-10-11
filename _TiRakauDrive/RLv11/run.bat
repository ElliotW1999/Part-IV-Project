@echo off
C:\Anaconda\python.exe RL-runner.py 1
C:\Anaconda\python.exe calculateLossCurve.py 
for /F "tokens=2" %%i in ('date /t') do set startdate=%%i
set starttime=%time%
for /l %%y in (1, 1, 100) do (
    for /l %%x in (1, 1, 20) do (
        C:\Anaconda\python.exe RL-runner.py 43
        C:\Anaconda\python.exe saveMeanSpeed.py
        C:\Anaconda\python.exe RL-runner.py 44
        C:\Anaconda\python.exe saveMeanSpeed.py
        C:\Anaconda\python.exe RL-runner.py 45
        C:\Anaconda\python.exe saveMeanSpeed.py
        C:\Anaconda\python.exe RL-runner.py 46
        C:\Anaconda\python.exe saveMeanSpeed.py
        C:\Anaconda\python.exe RL-runner.py 47
        C:\Anaconda\python.exe saveMeanSpeed.py
        
        C:\Anaconda\python.exe RL-runner.py 42
        C:\Anaconda\python.exe learn.py
        C:\Anaconda\python.exe RL-runner.py 41
        C:\Anaconda\python.exe learn.py
        C:\Anaconda\python.exe removeMeanSpeeds.py
    )
    C:\Anaconda\python.exe RL-runner.py 42
    C:\Anaconda\python.exe calculateLossCurve.py 
)
C:\Anaconda\python.exe analyzelosscurves.py
for /F "tokens=2" %%i in ('date /t') do set enddate=%%i
set endtime=%time%
echo start time is %startdate%:%starttime%
echo end time is %enddate%:%endtime%
pause
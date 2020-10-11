@echo off
<<<<<<< HEAD
C:\Anaconda\python.exe RL-runner.py 1
C:\Anaconda\python.exe calculateLossCurve.py 
=======
C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe RL-runner.py 1
C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe calculateLossCurve.py 
>>>>>>> 829bdf6fd3805b9151f095bd2d21307c99880617
for /F "tokens=2" %%i in ('date /t') do set startdate=%%i
set starttime=%time%
for /l %%y in (1, 1, 40) do (
    for /l %%y in (1, 1, 5) do (
        for /l %%x in (1, 1, 60) do (
<<<<<<< HEAD
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
=======
            C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe RL-runner.py 0
            C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe learn.py
        )
        C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe RL-runner.py 1
        C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe calculateLossCurve.py 
    )
    C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe RL-runner.py 1
    C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe learn.py
)
C:\Users\Elliot\Anaconda3\envs\PartIvProject\python.exe analyzelosscurves.py
>>>>>>> 829bdf6fd3805b9151f095bd2d21307c99880617
for /F "tokens=2" %%i in ('date /t') do set enddate=%%i
set endtime=%time%
echo start time is %startdate%:%starttime%
echo end time is %enddate%:%endtime%
pause
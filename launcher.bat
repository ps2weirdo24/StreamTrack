@echo off

REM %1 = channel , %2 = length of clips , %3 = quality

start python stathandler.py %1 %2 %3

timeout /t 5 /nobreak

for /F "Delims=, Tokens=1,2" %%a in (robot_talk.txt) do (set status=%%a & set workingdir=%%b
	)

GOTO %status%

:online

start Capture.bat %1 %3 "%workingdir%"

cmdow /TH

timeout /t %2 /nobreak

taskkill /fi "WINDOWTITLE eq stream_capture_%1" /f /t

start AfterCapture.bat %1 "%workingdir%"

start launcher.bat %1 %2 %3

EXIT

:offline

echo "%1's" stream was offline

EXIT
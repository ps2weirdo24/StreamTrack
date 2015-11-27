REM This file is to test running multiple stream captures at once, so far it has worked
@echo off

echo Starting first capture
start launcher.bat imaqtpie 1800 high

timeout /t 30 /nobreak

echo Starting second capture
start launcher.bat esl_lol 1800 high

timeout /t 30 /nobreak

echo Starting third capture
start launcher.bat grossie_gore 1800 high

timeout /t 2 /nobreak

exit
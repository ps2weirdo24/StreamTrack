REM This file is to test running multiple stream captures at once, so far it has worked
@echo off

echo Starting wingsofdeath capture

start launcher.bat wingsofdeath 120 high

timeout /t 15 /nobreak

echo Starting mushisgosu capture

start launcher.bat mushisgosu 120 high

echo endind this process

timeout /t 2 /nobreak

exit
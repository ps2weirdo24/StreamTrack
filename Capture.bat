@echo off

REM %1 = twitch.tv/{STREAM_NAME} %2 = quality

title stream_capture

cd "%3"

livestreamer -o "%1.flv" "twitch.tv/%1" %2


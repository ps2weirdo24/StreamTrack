@echo off

echo Stream capture complete!

ffmpeg -i "%2/%1.flv" "%2/%1.wav"

echo WAV file conversion complete!

REM ffmpeg -i "%2/%1.flv" "%2/%1.mp4"

REM echo MP4 file conversion complete!

EXIT
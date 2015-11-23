@echo off

echo Stream capture complete!

ffmpeg -i "%2/%1.flv" "%2/%1.wav"

echo WAV file conversion complete

ffmpeg -i "%2/%1.flv" -c copy -copyts -bsf:a aac_adtstoasc "%2/%1_fixed.mp4"

echo MP4 file conversion complete

timeout /t 5 /nobreak

set a=%2\%1.flv
set a=%a:/=\%

DEL /Q %a%

echo FLV File Deleted

EXIT

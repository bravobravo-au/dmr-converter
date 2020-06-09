@ECHO OFF

SET CC=C:\\Program Files\\mingw-w64\\x86_64-8.1.0-posix-seh-rt_v6-rev0\\mingw64\\bin\\gcc.exe
REM SET CC=C:\\Program Files (x86)\\mingw-w64\\i686-8.1.0-posix-dwarf-rt_v6-rev0\\mingw32\\bin\\gcc.exe

ECHO Setting CC To: %CC%


python -m nuitka --follow-imports --standalone --mingw64 --remove-output --recurse-all --assume-yes-for-downloads dmrconvert.py
PAUSE
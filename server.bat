@echo off
@echo Attempting to start the World_Server...
c:\python\python.exe server.py --seed 5778845986643073096
@echo Server stopping.
cleanup.bat

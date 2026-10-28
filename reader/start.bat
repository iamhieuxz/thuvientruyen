@echo off
rem Chay trang doc truyen local: mo file nay hoac go "reader\start.bat" trong F:\taitruyen
cd /d %~dp0..
set PYTHONIOENCODING=utf-8
python reader\server.py %*
pause

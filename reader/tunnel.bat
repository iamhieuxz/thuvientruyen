@echo off
rem Bat ca hai cong truyen (reader 8080 + VieNeu worker 8123) roi mo duong dan cong khai.
rem Quick tunnel: URL doi moi lan chay, va may tinh khong duoc ngu.
cd /d %~dp0..
set PYTHONIOENCODING=utf-8

curl -s --max-time 3 http://localhost:8080/api/ping | findstr baogiam-reader >nul 2>&1
if errorlevel 1 (
  echo Mo reader tren cong 8080...
  start "Doc truyen local" cmd /k python reader\server.py
  timeout /t 8 /nobreak >nul
) else (
  echo Reader 8080 da chay san.
)

echo VieNeu worker tu tai model qua /api/voices...
curl -s --max-time 30 http://localhost:8080/api/voices >nul 2>&1
curl -s --max-time 30 http://localhost:8080/api/voices | findstr /c:"ready" >nul && echo   VieNeu: ready || echo   VieNeu: dang tai, mo trang van nghe duoc sau

echo.
echo Dang xin duong dan Cloudflare...
echo URL cua lan nay cung duoc ghi vao: %~dp0tunnel.log
echo.
"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:8080 --no-autoupdate --logfile "%~dp0tunnel.log"

echo.
echo Dong cua so nay thi mat duong truy cap tu xa.
pause

@echo off
echo ============================================
echo    IPTV Server - Demarrage
echo ============================================
echo.

cd /d "%~dp0"

echo Installation des dependances...
pip install -r requirements.txt

echo.
echo Demarrage du serveur...
echo.

python server.py

pause

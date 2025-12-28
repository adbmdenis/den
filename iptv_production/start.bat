@echo off
echo ============================================
echo    IPTV SERVER PRODUCTION - Demarrage
echo ============================================
echo.

cd /d "%~dp0"

echo [1/3] Installation des dependances...
pip install -r requirements.txt

echo.
echo [2/3] Verification de la configuration...
if not exist .env (
    echo ATTENTION: Fichier .env non trouve!
    echo Copie de .env.example vers .env...
    copy .env.example .env
    echo.
    echo IMPORTANT: Editez .env et configurez vos parametres!
    pause
)

echo.
echo [3/3] Demarrage du serveur...
echo.
echo ============================================
echo    Serveur demarre sur http://localhost:8888
echo ============================================
echo.
echo Panel Admin: http://localhost:8888/admin
echo Espace Client: http://localhost:8888/client
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo ============================================
echo.

python server.py

pause

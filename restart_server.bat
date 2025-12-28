@echo off
echo ========================================
echo REDEMARRAGE DU SERVEUR IPTV
echo ========================================
echo.

echo [1/4] Arret de tous les processus Python...
taskkill /F /IM python.exe /T 2>nul
if %errorlevel% == 0 (
    echo    OK - Processus Python arretes
) else (
    echo    INFO - Aucun processus Python en cours
)
timeout /t 2 /nobreak >nul

echo.
echo [2/4] Verification du fichier admin_panel.py...
if exist "admin_panel.py" (
    echo    OK - admin_panel.py trouve
    for %%A in (admin_panel.py) do echo    Taille: %%~zA octets
) else (
    echo    ERREUR - admin_panel.py introuvable!
    pause
    exit /b 1
)

echo.
echo [3/4] Nettoyage du cache Python...
if exist "__pycache__" (
    rmdir /s /q "__pycache__" 2>nul
    echo    OK - Cache Python supprime
) else (
    echo    INFO - Pas de cache a nettoyer
)

echo.
echo [4/4] Demarrage du serveur...
echo.
echo ========================================
echo SERVEUR DEMARRE
echo ========================================
echo.
echo Ouvrez votre navigateur sur:
echo   http://192.168.1.19:8888/admin
echo.
echo Appuyez sur Ctrl+C pour arreter
echo ========================================
echo.

python server.py

pause

@echo off
cls
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║         REDEMARRAGE COMPLET DU SERVEUR IPTV                  ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo.

echo [ETAPE 1/6] Arret de tous les processus Python...
echo.
taskkill /F /IM python.exe /T >nul 2>&1
if %errorlevel% == 0 (
    echo    ✓ Processus Python arretes
) else (
    echo    ℹ Aucun processus Python en cours
)
timeout /t 2 /nobreak >nul
echo.

echo [ETAPE 2/6] Nettoyage du cache Python...
echo.
if exist "__pycache__" (
    rmdir /s /q "__pycache__" >nul 2>&1
    echo    ✓ Cache __pycache__ supprime
)
if exist "*.pyc" (
    del /q "*.pyc" >nul 2>&1
    echo    ✓ Fichiers .pyc supprimes
)
echo    ✓ Cache nettoye
echo.

echo [ETAPE 3/6] Verification du fichier admin_panel.py...
echo.
if exist "admin_panel.py" (
    for %%A in (admin_panel.py) do (
        echo    ✓ Fichier trouve: %%~zA octets
        echo    ✓ Modifie: %%~tA
    )
) else (
    echo    ✗ ERREUR: admin_panel.py introuvable!
    pause
    exit /b 1
)
echo.

echo [ETAPE 4/6] Test du fichier admin_panel.py...
echo.
python debug_html_output.py 2>nul | findstr /C:"Blocs <script>" /C:"function showModal"
echo.

echo [ETAPE 5/6] Preparation du demarrage...
echo.
echo    ✓ Tous les processus arretes
echo    ✓ Cache nettoye
echo    ✓ Fichier verifie
echo.

echo [ETAPE 6/6] Demarrage du serveur...
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║                    SERVEUR DEMARRE                           ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo   Ouvrez votre navigateur sur:
echo.
echo   ► http://192.168.1.19:8888/admin
echo.
echo   IMPORTANT:
echo   1. Videz le cache du navigateur (Ctrl+Shift+Delete)
echo   2. Rechargez la page (Ctrl+F5)
echo.
echo   Appuyez sur Ctrl+C pour arreter le serveur
echo.
echo ══════════════════════════════════════════════════════════════
echo.

python server.py

echo.
echo Serveur arrete.
pause

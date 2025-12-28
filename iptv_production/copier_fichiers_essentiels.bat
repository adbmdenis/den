@echo off
chcp 65001 >nul
echo ============================================================
echo COPIE DES FICHIERS ESSENTIELS POUR NOUVEAU PROJET IPTV
echo ============================================================
echo.

REM Demander le chemin de destination
set /p DEST="Entrez le chemin du nouveau projet (ex: C:\mon_nouveau_iptv): "

REM Vérifier si le dossier existe, sinon le créer
if not exist "%DEST%" (
    echo.
    echo 📁 Création du dossier: %DEST%
    mkdir "%DEST%"
)

echo.
echo 📦 Copie des fichiers essentiels...
echo.

REM Copier les fichiers Python principaux
echo ✅ Copie de server.py
copy /Y "server.py" "%DEST%\" >nul

echo ✅ Copie de config.py
copy /Y "config.py" "%DEST%\" >nul

echo ✅ Copie de database.py
copy /Y "database.py" "%DEST%\" >nul

echo ✅ Copie de admin_panel.py
copy /Y "admin_panel.py" "%DEST%\" >nul

echo ✅ Copie de vavoo_service.py
copy /Y "vavoo_service.py" "%DEST%\" >nul

echo ✅ Copie de multi_service.py
copy /Y "multi_service.py" "%DEST%\" >nul

REM Copier les fichiers de configuration
echo ✅ Copie de .env.example
copy /Y ".env.example" "%DEST%\" >nul

echo ✅ Copie de requirements.txt
copy /Y "requirements.txt" "%DEST%\" >nul

echo ✅ Copie de .gitignore
copy /Y ".gitignore" "%DEST%\" >nul

REM Copier les scripts de démarrage
echo ✅ Copie de start.bat
copy /Y "start.bat" "%DEST%\" >nul

echo ✅ Copie de start.sh
copy /Y "start.sh" "%DEST%\" >nul

REM Copier les scripts utilitaires (optionnel)
echo ✅ Copie de reset_database.py
copy /Y "reset_database.py" "%DEST%\" >nul

echo ✅ Copie de test_server.py
copy /Y "test_server.py" "%DEST%\" >nul

REM Copier la documentation
echo ✅ Copie de README.md
copy /Y "README.md" "%DEST%\" >nul

echo.
echo ============================================================
echo ✅ COPIE TERMINÉE!
echo ============================================================
echo.
echo 📁 Fichiers copiés dans: %DEST%
echo.
echo 📋 PROCHAINES ÉTAPES:
echo.
echo 1. Aller dans le nouveau dossier:
echo    cd "%DEST%"
echo.
echo 2. Créer le fichier .env:
echo    copy .env.example .env
echo.
echo 3. Éditer .env avec vos paramètres:
echo    notepad .env
echo.
echo 4. Installer les dépendances:
echo    pip install -r requirements.txt
echo.
echo 5. Démarrer le serveur:
echo    start.bat
echo.
echo ============================================================
pause

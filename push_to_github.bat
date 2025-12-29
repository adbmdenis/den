@echo off
echo ========================================
echo   PUSH VERS GITHUB - SERVEUR IPTV
echo ========================================
echo.

cd /d "%~dp0"

echo [1/7] Initialisation du depot Git...
git init
if errorlevel 1 (
    echo Erreur lors de l'initialisation Git
    pause
    exit /b 1
)

echo.
echo [2/7] Configuration Git...
git config user.name "adbmdenis"
git config user.email "adbmdenis@users.noreply.github.com"

echo.
echo [3/7] Ajout des fichiers...
git add .
if errorlevel 1 (
    echo Erreur lors de l'ajout des fichiers
    pause
    exit /b 1
)

echo.
echo [4/7] Commit des changements...
git commit -m "Initial commit - Serveur IPTV complet avec panel admin"
if errorlevel 1 (
    echo Erreur lors du commit
    pause
    exit /b 1
)

echo.
echo [5/7] Creation de la branche main...
git branch -M main
if errorlevel 1 (
    echo Erreur lors de la creation de la branche
    pause
    exit /b 1
)

echo.
echo [6/7] Ajout du remote origin...
git remote add origin https://github.com/adbmdenis/den.git
if errorlevel 1 (
    echo Remote deja existant, on continue...
    git remote set-url origin https://github.com/adbmdenis/den.git
)

echo.
echo [7/7] Push vers GitHub...
echo.
echo ATTENTION: Vous allez etre invite a entrer vos identifiants GitHub
echo.
git push -u origin main
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERREUR LORS DU PUSH
    echo ========================================
    echo.
    echo Possible causes:
    echo - Le depot existe deja sur GitHub
    echo - Identifiants incorrects
    echo - Pas de connexion internet
    echo.
    echo Solutions:
    echo 1. Verifiez que le depot est vide sur GitHub
    echo 2. Utilisez un Personal Access Token au lieu du mot de passe
    echo 3. Ou utilisez: git push -u origin main --force
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   PUSH REUSSI!
echo ========================================
echo.
echo Votre code est maintenant sur GitHub:
echo https://github.com/adbmdenis/den
echo.
pause

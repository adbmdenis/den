@echo off
echo ==========================================
echo   PUSH FINAL SUR GITHUB
echo ==========================================
echo.

REM Ajouter tous les fichiers
echo Ajout de tous les fichiers...
git add .

REM Créer le commit
echo.
echo Creation du commit...
git commit -m "Fix: Correction complete - Identifiants + Reset DB + Documentation"

REM Pousser sur GitHub
echo.
echo Push sur GitHub...
git push origin main

echo.
echo ==========================================
echo   PUSH TERMINE !
echo ==========================================
echo.
echo Render va redéployer automatiquement.
echo Attendez 5-10 minutes puis suivez LISEZ_MOI_DABORD.md
echo.

pause

# Redémarrage du serveur IPTV avec nettoyage complet

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "REDEMARRAGE DU SERVEUR IPTV" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Arrêter tous les processus Python
Write-Host "[1/5] Arret des processus Python..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    $pythonProcesses | Stop-Process -Force
    Write-Host "   OK - $($pythonProcesses.Count) processus Python arretes" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "   INFO - Aucun processus Python en cours" -ForegroundColor Gray
}

# 2. Vérifier le fichier admin_panel.py
Write-Host ""
Write-Host "[2/5] Verification du fichier admin_panel.py..." -ForegroundColor Yellow
if (Test-Path "admin_panel.py") {
    $fileInfo = Get-Item "admin_panel.py"
    Write-Host "   OK - admin_panel.py trouve" -ForegroundColor Green
    Write-Host "   Taille: $($fileInfo.Length) octets" -ForegroundColor Gray
    Write-Host "   Modifie: $($fileInfo.LastWriteTime)" -ForegroundColor Gray
    
    # Vérifier le contenu
    $content = Get-Content "admin_panel.py" -Raw
    $scriptCount = ([regex]::Matches($content, "<script>")).Count
    Write-Host "   Blocs <script> dans le fichier: $scriptCount" -ForegroundColor Gray
    
    if ($scriptCount -ne 1) {
        Write-Host "   ATTENTION - Le fichier devrait avoir 1 seul bloc <script>!" -ForegroundColor Red
    }
} else {
    Write-Host "   ERREUR - admin_panel.py introuvable!" -ForegroundColor Red
    Read-Host "Appuyez sur Entree pour quitter"
    exit 1
}

# 3. Nettoyer le cache Python
Write-Host ""
Write-Host "[3/5] Nettoyage du cache Python..." -ForegroundColor Yellow
$cacheDeleted = 0
if (Test-Path "__pycache__") {
    Remove-Item "__pycache__" -Recurse -Force
    $cacheDeleted++
}
if (Test-Path "*.pyc") {
    Remove-Item "*.pyc" -Force
    $cacheDeleted++
}
if ($cacheDeleted -gt 0) {
    Write-Host "   OK - Cache Python supprime" -ForegroundColor Green
} else {
    Write-Host "   INFO - Pas de cache a nettoyer" -ForegroundColor Gray
}

# 4. Vérifier les dépendances
Write-Host ""
Write-Host "[4/5] Verification des dependances..." -ForegroundColor Yellow
try {
    python -c "import config, database, multi_service, admin_panel" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   OK - Tous les modules peuvent etre importes" -ForegroundColor Green
    } else {
        Write-Host "   ERREUR - Probleme d'import des modules" -ForegroundColor Red
    }
} catch {
    Write-Host "   ERREUR - $($_.Exception.Message)" -ForegroundColor Red
}

# 5. Démarrer le serveur
Write-Host ""
Write-Host "[5/5] Demarrage du serveur..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SERVEUR DEMARRE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ouvrez votre navigateur sur:" -ForegroundColor White
Write-Host "  http://192.168.1.19:8888/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arreter" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Démarrer avec logs
python start_with_logs.py

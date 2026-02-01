# Script d'installation automatique de Tesseract OCR pour Windows
# Usage: powershell -ExecutionPolicy Bypass -File install_tesseract.ps1

Write-Host "Installation de Tesseract OCR pour Windows..." -ForegroundColor Green

# URL de téléchargement du build UB-Mannheim (recommandé)
$downloadUrl = "https://github.com/UB-Mannheim/tesseract/wiki"
$installerPath = "$env:TEMP\tesseract-installer.exe"

Write-Host @"
╔════════════════════════════════════════════════════════════════════╗
║  Tesseract OCR - Installation Windows                              ║
╚════════════════════════════════════════════════════════════════════╝

Ce script va télécharger et installer Tesseract OCR.

Options disponibles:

  1) Télécharger automatiquement via URL (recommandé)
  2) Ouvrir la page GitHub de téléchargement (manuel)
  3) Quitter

"@

$choice = Read-Host "Choisissez une option (1-3)"

if ($choice -eq "1") {
    Write-Host "Recherche du dernier installeur Tesseract..." -ForegroundColor Yellow
    
    # Récupérer l'URL de la dernière version depuis GitHub API
    $releases = Invoke-RestMethod -Uri "https://api.github.com/repos/UB-Mannheim/tesseract/releases/latest" -ErrorAction Stop
    $downloadUrl = $releases.assets | Where-Object { $_.name -like "*w64-setup*.exe" } | Select-Object -First 1 -ExpandProperty browser_download_url
    
    if ($null -eq $downloadUrl) {
        Write-Host "Impossible de trouver l'installeur automatiquement." -ForegroundColor Red
        Write-Host "Veuillez télécharger manuellement depuis: https://github.com/UB-Mannheim/tesseract/releases" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "URL trouvée: $downloadUrl" -ForegroundColor Cyan
    Write-Host "Téléchargement en cours..." -ForegroundColor Yellow
    
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -ErrorAction Stop
        Write-Host "Téléchargement terminé!" -ForegroundColor Green
        
        Write-Host "Lancement de l'installeur..." -ForegroundColor Yellow
        Start-Process -FilePath $installerPath -Wait
        
        Write-Host @"
Installation terminée!

✓ Tesseract devrait être installé en: C:\Program Files\Tesseract-OCR
✓ Redémarrez votre terminal ou IDE
✓ Relancez: python main.py

"@ -ForegroundColor Green
        
    } catch {
        Write-Host "Erreur lors du téléchargement: $_" -ForegroundColor Red
        exit 1
    }
    
} elseif ($choice -eq "2") {
    Write-Host "Ouverture de la page de téléchargement..." -ForegroundColor Yellow
    Start-Process "https://github.com/UB-Mannheim/tesseract/releases"
    Write-Host @"
Instructions:
1) Téléchargez tesseract-ocr-w64-setup-v*.exe
2) Exécutez l'installeur et suivez l'assistant
3) Acceptez l'installation en C:\Program Files\Tesseract-OCR
4) Redémarrez votre terminal
5) Relancez: python main.py
"@ -ForegroundColor Cyan
    
} elseif ($choice -eq "3") {
    Write-Host "Installation annulée." -ForegroundColor Yellow
    exit 0
    
} else {
    Write-Host "Option invalide." -ForegroundColor Red
    exit 1
}

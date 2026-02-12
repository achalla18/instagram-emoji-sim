# ═══════════════════════════════════════════════════
# Emoji Reactions — Windows Setup Script
# Run: powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
# ═══════════════════════════════════════════════════

Write-Host ""
Write-Host "  ========================================" -ForegroundColor Cyan
Write-Host "   Emoji Reactions -- Setup" -ForegroundColor Cyan
Write-Host "  ========================================" -ForegroundColor Cyan
Write-Host ""

# ── Check Python ──
Write-Host "  [1/3] Checking Python..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "  [!] Python not found." -ForegroundColor Red
    Write-Host "  Please install Python 3.10+ from https://python.org" -ForegroundColor Red
    Write-Host "  Make sure to check 'Add Python to PATH' during install." -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

$pyVersion = python --version 2>&1
Write-Host "  Found: $pyVersion" -ForegroundColor Green

# ── Install optional dependencies ──
Write-Host ""
Write-Host "  [2/3] Installing optional dependencies..." -ForegroundColor Yellow
try {
    python -m pip install --quiet --upgrade pip 2>$null
    python -m pip install --quiet pillow 2>$null
    Write-Host "  Pillow installed (optional, for image export)" -ForegroundColor Green
} catch {
    Write-Host "  Pillow install skipped (not required)" -ForegroundColor DarkGray
}

# ── Verify project structure ──
Write-Host ""
Write-Host "  [3/3] Verifying project files..." -ForegroundColor Yellow

$requiredFiles = @(
    "src\python\app.py",
    "src\python\reactions.py",
    "src\python\config.py",
    "src\web\index.html",
    "src\web\css\style.css",
    "src\web\js\app.js",
    "src\web\js\particles.js",
    "src\web\js\audio.js",
    "config\settings.json"
)

$projectRoot = Split-Path -Parent $PSScriptRoot
$allPresent = $true

foreach ($file in $requiredFiles) {
    $fullPath = Join-Path $projectRoot $file
    if (Test-Path $fullPath) {
        Write-Host "  OK  $file" -ForegroundColor DarkGreen
    } else {
        Write-Host "  MISSING  $file" -ForegroundColor Red
        $allPresent = $false
    }
}

Write-Host ""
if ($allPresent) {
    Write-Host "  ========================================" -ForegroundColor Green
    Write-Host "  Setup complete! All files verified." -ForegroundColor Green
    Write-Host "  ========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "  To run the Desktop app:" -ForegroundColor Cyan
    Write-Host "    scripts\run-desktop.bat" -ForegroundColor White
    Write-Host ""
    Write-Host "  To run the Web version:" -ForegroundColor Cyan
    Write-Host "    scripts\run-web.bat" -ForegroundColor White
    Write-Host "    Then open http://localhost:8080" -ForegroundColor DarkGray
} else {
    Write-Host "  [!] Some files are missing. Re-download the project." -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

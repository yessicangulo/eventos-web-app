# Script de activación automática del entorno virtual
# Este archivo se ejecuta automáticamente cuando entras al directorio backend

$backendPath = "C:\Users\Dell\OneDrive\Documentos\Datos\backend"
$currentPath = Get-Location

# Solo activar si estamos en el directorio backend o un subdirectorio
if ($currentPath.Path -like "$backendPath*") {
    # Verificar si el entorno ya está activo
    if (-not $env:VIRTUAL_ENV) {
        $envPath = poetry env info --path 2>$null
        if ($envPath -and (Test-Path "$envPath\Scripts\activate.ps1")) {
            & "$envPath\Scripts\activate.ps1"
            Write-Host "✓ Entorno virtual activado automáticamente" -ForegroundColor Green
        }
    }
}

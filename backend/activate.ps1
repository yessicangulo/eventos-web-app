# Script para activar el entorno virtual de Poetry
# Uso: .\activate.ps1

$envPath = poetry env info --path
if ($envPath) {
    & "$envPath\Scripts\activate.ps1"
    Write-Host "Entorno virtual activado: $envPath" -ForegroundColor Green
    Write-Host "Para verificar, ejecuta: python -c 'import sys; print(sys.executable)'" -ForegroundColor Yellow
} else {
    Write-Host "Error: No se encontró el entorno virtual. Ejecuta 'poetry install' primero." -ForegroundColor Red
}

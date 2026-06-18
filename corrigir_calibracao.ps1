# corrigir_calibracao.ps1
Write-Host "CORRIGINDO CALIBRAÇÃO" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan

Write-Host ""
Write-Host "1. Verificando se Programa Y está rodando..." -ForegroundColor Yellow

$process = Get-Process | Where-Object { $_.ProcessName -like "*python*" }
if ($process) {
    Write-Host "   ✅ Python está rodando" -ForegroundColor Green
} else {
    Write-Host "   ❌ Python NÃO está rodando!" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Abra um novo terminal e execute:" -ForegroundColor Yellow
    Write-Host "   cd programa_y" -ForegroundColor White
    Write-Host "   python form_app.py" -ForegroundColor White
}

Write-Host ""
Write-Host "2. Atualizando config.json..." -ForegroundColor Yellow

# Encontrar o título correto usando Python
$script = @"
import win32gui
import json

def encontrar_titulo():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Programa Y" in title or "Formulário" in title:
                windows.append(title)
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows[0] if windows else None

titulo = encontrar_titulo()
if titulo:
    print(titulo)
"@

$titulo = python -c $script

if ($titulo) {
    Write-Host "   ✅ Título encontrado: $titulo" -ForegroundColor Green
    
    # Atualiza o config.json
    $configPath = "programa_x\config.json"
    if (Test-Path $configPath) {
        $config = Get-Content $configPath | ConvertFrom-Json
        $config.window_title = $titulo
        $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
        Write-Host "   ✅ Config atualizado!" -ForegroundColor Green
    }
} else {
    Write-Host "   ❌ Título não encontrado!" -ForegroundColor Red
}

Write-Host ""
Write-Host "=====================" -ForegroundColor Cyan
Write-Host "PRONTO PARA CALIBRAR!" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Agora no Programa X:" -ForegroundColor Yellow
Write-Host "1. Escolha opção 2" -ForegroundColor White
Write-Host "2. Pressione ENTER" -ForegroundColor White
Write-Host "3. Mova o mouse para cada campo e pressione ENTER" -ForegroundColor White
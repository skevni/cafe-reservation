# Запуск продакшен-режима: PostgreSQL + FastAPI

Write-Host "Запуск в режиме продакшена (PostgreSQL)" -ForegroundColor Green

# 1. Проверка наличия Docker
Write-Host "Проверка установки Docker..." -ForegroundColor Cyan
if (!(Get-Command "docker" -ErrorAction SilentlyContinue)) {
    Write-Host "Docker не установлен или не доступен в PATH." -ForegroundColor Red
    Write-Host "Установите Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}
Write-Host "Docker найден" -ForegroundColor Green

# 2. Установка переменных окружения
$env:COMPOSE_FILE = "docker-compose.yml;docker-compose.prod.yml"
$env:ENVIRONMENT = "prod"

# 3. Запуск Docker Compose в фоне
Write-Host "Запуск контейнеров в фоновом режиме (-d)..." -ForegroundColor Cyan
docker compose down --remove-orphans | Out-Null
if (docker compose up -d --build) {
    Write-Host "Контейнеры запущены в фоне" -ForegroundColor Green
} else {
    Write-Host "Ошибка при запуске контейнеров" -ForegroundColor Red
    exit 1
}

# 4. Ожидание готовности API
$apiUrl = "http://localhost:8000/health"
$maxRetries = 30
$retryDelay = 5  # секунд
$success = $false

Write-Host "Ожидание готовности API на $apiUrl..." -ForegroundColor Cyan

for ($i = 1; $i -le $maxRetries; $i++) {
    Write-Host "Попытка $i из $maxRetries..." -ForegroundColor DarkGray
    try {
        $response = Invoke-RestMethod -Uri $apiUrl -Method Get -TimeoutSec 10
        if ($response.status -eq "ok") {
            $success = $true
            break
        }
    } catch {
        # Игнорируем ошибки — сервис ещё может не отвечать
    }
    Start-Sleep -Seconds $retryDelay
}

# 5. Результат
if ($success) {
    Write-Host "API готов к работе!" -ForegroundColor Green
    Write-Host "Откройте: http://localhost:8000" -ForegroundColor Yellow
} else {
    Write-Host "API не ответил за отведённое время." -ForegroundColor Red
    Write-Host "Проверьте логи: docker compose logs app" -ForegroundColor Yellow
    exit 1
}
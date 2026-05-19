Write-Host "Запуск в режиме разработки (SQLite)" -ForegroundColor Green

$env:ENVIRONMENT = "dev"
docker compose up --build
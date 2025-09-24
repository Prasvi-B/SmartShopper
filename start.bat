@echo off
REM SmartShopper Quick Start Script for Windows

echo 🛒 SmartShopper - Quick Start
echo =============================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Desktop with Compose.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ✅ .env file created. Please edit it with your configuration.
)

REM Create data directory
if not exist data mkdir data

echo 🚀 Starting SmartShopper services...

REM Start services
docker-compose up --build -d

echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

echo 🔍 Checking service status...
docker-compose ps

echo.
echo 🎉 SmartShopper is running!
echo 📖 Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 🛠️  Useful commands:
echo    View logs: docker-compose logs -f
echo    Stop services: docker-compose down
echo    Restart services: docker-compose restart
echo.
pause
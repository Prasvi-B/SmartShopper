@echo off
echo 🚀 Setting up SmartShopper Development Environment...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker first.
    exit /b 1
)

REM Create required directories
echo 📁 Creating required directories...
if not exist "backend\logs" mkdir "backend\logs"
if not exist "backend\models" mkdir "backend\models"
if not exist "data\mongodb" mkdir "data\mongodb"
if not exist "data\redis" mkdir "data\redis"

REM Create .env file if it doesn't exist
if not exist "backend\.env" (
    echo 📝 Creating .env file...
    (
        echo # Environment Configuration
        echo ENVIRONMENT=development
        echo.
        echo # Database Configuration
        echo MONGODB_URL=mongodb://smartshopper:smartshopper123@localhost:27017/smartshopper?authSource=admin
        echo DATABASE_NAME=smartshopper
        echo.
        echo # Security Configuration
        echo SECRET_KEY=your-super-secret-key-change-this-in-production
        echo ALGORITHM=HS256
        echo ACCESS_TOKEN_EXPIRE_MINUTES=30
        echo REFRESH_TOKEN_EXPIRE_DAYS=7
        echo.
        echo # API Configuration
        echo DEBUG=true
        echo ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
        echo.
        echo # External API Keys ^(Add your keys here^)
        echo AMAZON_API_KEY=your-amazon-api-key
        echo FLIPKART_API_KEY=your-flipkart-api-key
        echo MYNTRA_API_KEY=your-myntra-api-key
        echo.
        echo # Redis Configuration
        echo REDIS_URL=redis://localhost:6379/0
        echo.
        echo # Email Configuration ^(Optional^)
        echo SMTP_HOST=smtp.gmail.com
        echo SMTP_PORT=587
        echo SMTP_USERNAME=
        echo SMTP_PASSWORD=
        echo.
        echo # Logging
        echo LOG_LEVEL=INFO
        echo LOG_FILE=logs/smartshopper.log
    ) > "backend\.env"
    echo ✅ .env file created
) else (
    echo ⚠️  .env file already exists, skipping...
)

REM Start MongoDB and Redis services
echo 🔧 Starting MongoDB and Redis services...
docker-compose up -d mongodb redis

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check if services are running
docker-compose ps | findstr "smartshopper-mongo" | findstr "Up" >nul
if not errorlevel 1 (
    echo ✅ MongoDB is running
) else (
    echo ❌ MongoDB failed to start
)

docker-compose ps | findstr "smartshopper-redis" | findstr "Up" >nul
if not errorlevel 1 (
    echo ✅ Redis is running
) else (
    echo ❌ Redis failed to start
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
cd backend
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo ✅ Python dependencies installed
) else (
    echo ⚠️  requirements.txt not found, skipping Python dependencies
)
cd ..

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
cd frontend
if exist "package.json" (
    npm install
    echo ✅ Node.js dependencies installed
) else (
    echo ⚠️  package.json not found, skipping Node.js dependencies
)
cd ..

echo.
echo 🎉 SmartShopper development environment setup complete!
echo.
echo 🔗 Quick Start Commands:
echo   Start all services:     docker-compose up -d
echo   Start backend only:     cd backend ^&^& python main.py
echo   Start frontend only:    cd frontend ^&^& npm run dev
echo   View logs:              docker-compose logs -f
echo   Stop services:          docker-compose down
echo.
echo 🌐 Application URLs:
echo   Frontend:               http://localhost:3000
echo   Backend API:            http://localhost:8000
echo   API Documentation:      http://localhost:8000/docs
echo   MongoDB:                mongodb://localhost:27017
echo   Redis:                  redis://localhost:6379
echo.
echo 📚 Next Steps:
echo   1. Update API keys in backend\.env
echo   2. Run: docker-compose up -d
echo   3. Open http://localhost:3000 in your browser

pause
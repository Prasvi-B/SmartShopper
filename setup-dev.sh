#!/bin/bash
# SmartShopper Development Setup Script

echo "🚀 Setting up SmartShopper Development Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create required directories
echo "📁 Creating required directories..."
mkdir -p backend/logs
mkdir -p backend/models
mkdir -p data/mongodb
mkdir -p data/redis

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating .env file..."
    cat > backend/.env << EOL
# Environment Configuration
ENVIRONMENT=development

# Database Configuration
MONGODB_URL=mongodb://smartshopper:smartshopper123@localhost:27017/smartshopper?authSource=admin
DATABASE_NAME=smartshopper

# Security Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production-$(openssl rand -base64 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API Configuration
DEBUG=true
ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# External API Keys (Add your keys here)
AMAZON_API_KEY=your-amazon-api-key
FLIPKART_API_KEY=your-flipkart-api-key
MYNTRA_API_KEY=your-myntra-api-key

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/smartshopper.log
EOL
    echo "✅ .env file created"
else
    echo "⚠️  .env file already exists, skipping..."
fi

# Start MongoDB and Redis services
echo "🔧 Starting MongoDB and Redis services..."
docker-compose up -d mongodb redis

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "smartshopper-mongo.*Up"; then
    echo "✅ MongoDB is running"
else
    echo "❌ MongoDB failed to start"
fi

if docker-compose ps | grep -q "smartshopper-redis.*Up"; then
    echo "✅ Redis is running"
else
    echo "❌ Redis failed to start"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Python dependencies installed"
else
    echo "⚠️  requirements.txt not found, skipping Python dependencies"
fi
cd ..

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
if [ -f "package.json" ]; then
    npm install
    echo "✅ Node.js dependencies installed"
else
    echo "⚠️  package.json not found, skipping Node.js dependencies"
fi
cd ..

echo ""
echo "🎉 SmartShopper development environment setup complete!"
echo ""
echo "🔗 Quick Start Commands:"
echo "  Start all services:     docker-compose up -d"
echo "  Start backend only:     cd backend && python main.py"
echo "  Start frontend only:    cd frontend && npm run dev"
echo "  View logs:              docker-compose logs -f"
echo "  Stop services:          docker-compose down"
echo ""
echo "🌐 Application URLs:"
echo "  Frontend:               http://localhost:3000"
echo "  Backend API:            http://localhost:8000"
echo "  API Documentation:      http://localhost:8000/docs"
echo "  MongoDB:                mongodb://localhost:27017"
echo "  Redis:                  redis://localhost:6379"
echo ""
echo "📚 Next Steps:"
echo "  1. Update API keys in backend/.env"
echo "  2. Run: docker-compose up -d"
echo "  3. Open http://localhost:3000 in your browser"
# SmartShopper – Price & Review Analyzer

A comprehensive full-stack web application that helps users make informed purchasing decisions by comparing prices across multiple e-commerce platforms and analyzing product reviews using advanced sentiment analysis.

## 🚀 Features

### 🔐 Authentication & User Management
- **Secure User Registration & Login**: JWT-based authentication with refresh tokens
- **Comprehensive User Profiles**: Personal information, preferences, and settings
- **Role-Based Access Control**: USER, ADMIN, and MODERATOR roles with different permissions
- **Password Security**: bcrypt hashing with strong password requirements
- **User Preferences**: Personalized categories, brands, and platform preferences

### 🛍️ Core Shopping Features
- **Smart Product Search**: Full-text search with advanced filtering and user context
- **Multi-Platform Price Comparison**: Compare prices across Amazon, Flipkart, and Myntra
- **Intelligent Review Analysis**: AI-powered sentiment analysis of product reviews
- **Personal Wishlists**: Save and organize favorite products with user accounts
- **Smart Price Alerts**: User-specific notifications when prices drop below target
- **Search History**: Track and revisit previous searches for logged-in users

### 📊 Analytics & Intelligence
- **Sentiment Analysis**: Advanced NLP for review sentiment classification
- **User Dashboard**: Personal statistics, activity overview, and insights
- **Product Intelligence**: Rating distributions, sentiment summaries, and trends
- **Personalized Recommendations**: Future ML-based suggestions using user history

### 🎨 Modern UI/UX
- **Smart Minimal Glow Theme**: Beautiful glassmorphism design with gradients
- **Dark/Light Mode**: Automatic theme switching with user preferences
- **Responsive Design**: Mobile-first, fully responsive across all devices
- **Interactive Components**: Smooth animations and transitions

## 🛠️ Tech Stack

### Frontend
- **React 18+** with Vite for fast development
- **Tailwind CSS** for modern styling
- **React Query** for state management and API caching
- **React Router** for navigation
- **Recharts** for data visualization

### Backend
- **FastAPI** for high-performance async API
- **MongoDB** with **Beanie ODM** for document database
- **JWT Authentication** with refresh token support
- **Pydantic** for data validation and serialization
- **Redis** for caching and session management
- **Celery** for background task processing
- **bcrypt** for secure password hashing

### Machine Learning
- **Hugging Face Transformers** (DistilBERT/RoBERTa) for advanced sentiment analysis
- **Scikit-learn** for baseline models
- **TensorFlow/PyTorch** for deep learning models

### DevOps & Deployment
- **Docker & Docker Compose** for containerization
- **GitHub Actions** for CI/CD
- **Render/Railway/Heroku** for cloud deployment

### Data & Scraping
- **Scrapy** for robust web scraping
- **BeautifulSoup4** for HTML parsing
- **Requests** for HTTP operations

## 📁 Project Structure

```
SmartShopper/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   └── utils/          # Utility functions
│   └── package.json
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── routes/         # API endpoints
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── database/       # Database configuration
│   └── requirements.txt
├── ml/                     # Machine Learning models and training
│   ├── models/            # Trained model artifacts
│   ├── notebooks/         # Jupyter notebooks for experimentation
│   └── train.py          # Training scripts
├── scrapers/              # Web scraping modules
│   ├── amazon_scraper.py
│   ├── flipkart_scraper.py
│   └── utils/
├── deployment/            # Docker and deployment configurations
│   ├── Dockerfile.*
│   └── docker-compose.yml
└── docs/                 # Documentation and architecture diagrams
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Redis (for local development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/SmartShopper.git
   cd SmartShopper
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database Setup**
   ```bash
   cd backend
   python -m alembic upgrade head
   ```

### Running the Application

#### Option 1: Docker Compose (Recommended)
```bash
docker-compose up --build
```

#### Option 2: Manual Setup
```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 3: Start Frontend
cd frontend
npm run dev

# Terminal 4: Start Celery Worker (for background tasks)
cd backend
celery -A app.tasks worker --loglevel=info
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📊 Development Phases

### ✅ Phase 0: Setup & Preparation
- [x] Repository structure setup
- [x] Development environment configuration
- [x] Docker containerization

### ✅ Phase 1: MVP Development
- [x] Basic FastAPI backend with mock data endpoints
- [x] React frontend with Smart Minimal Glow theme
- [x] Modern UI components with glassmorphism effects
- [x] Responsive design with dark/light mode toggle
- [x] Professional search functionality
- [x] Simple ML baseline model ready
- [x] End-to-end search flow implementation

### 📅 Upcoming Phases
- **Phase 2**: Real scraping & data ingestion
- **Phase 3**: Advanced ML model improvements
- **Phase 4**: Frontend enhancements & UX
- **Phase 5**: Background jobs & price alerts
- **Phase 6**: Testing & security hardening
- **Phase 7**: Production deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who help make this project better
- Inspired by the need for transparent e-commerce price comparison
- Built with love for the developer community

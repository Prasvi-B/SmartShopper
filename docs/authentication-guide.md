# SmartShopper Authentication & User Management Guide

## 🔐 Authentication System Overview

SmartShopper now features a comprehensive user authentication and management system built with **MongoDB**, **FastAPI**, and **JWT tokens**. This guide covers the complete authentication flow and user features.

## 🏗️ Architecture

### Database: MongoDB
- **Primary Database**: MongoDB with Beanie ODM (async)
- **Authentication**: JWT tokens with refresh token support
- **User Roles**: USER, ADMIN, MODERATOR
- **Security**: Password hashing with bcrypt, role-based access control

### Key Components
- **Backend**: FastAPI with async/await support
- **Database ODM**: Beanie (async MongoDB ODM)
- **Authentication**: JWT with HTTP Bearer tokens
- **Password Security**: bcrypt hashing
- **Validation**: Pydantic models with comprehensive validation

## 📊 Database Schema

### User Document
```javascript
{
  _id: ObjectId,
  username: String (unique),
  email: String (unique),
  full_name: String?,
  hashed_password: String,
  phone_number: String?,
  date_of_birth: Date?,
  role: Enum["user", "admin", "moderator"],
  is_active: Boolean,
  is_verified: Boolean,
  created_at: Date,
  updated_at: Date,
  last_login: Date?
}
```

### User Preferences Document
```javascript
{
  _id: ObjectId,
  user_id: ObjectId (ref: User),
  preferred_categories: [String],
  preferred_brands: [String],
  price_range_min: Float?,
  price_range_max: Float?,
  preferred_platforms: [Enum],
  email_notifications: Boolean,
  push_notifications: Boolean,
  newsletter_subscription: Boolean,
  created_at: Date,
  updated_at: Date
}
```

### Product & Related Documents
```javascript
// Product
{
  _id: ObjectId,
  name: String,
  description: String?,
  category: String?,
  brand: String?,
  image_url: String?,
  created_at: Date,
  updated_at: Date
}

// Offer
{
  _id: ObjectId,
  product_id: ObjectId (ref: Product),
  platform: Enum["amazon", "flipkart", "myntra"],
  url: String,
  price: Float,
  original_price: Float?,
  discount_percentage: Float?,
  availability: String,
  seller_name: String?,
  shipping_cost: Float,
  created_at: Date,
  updated_at: Date
}

// Review
{
  _id: ObjectId,
  product_id: ObjectId (ref: Product),
  platform: Enum,
  reviewer_name: String?,
  rating: Int (1-5),
  title: String?,
  content: String,
  helpful_votes: Int,
  verified_purchase: Boolean,
  review_date: Date?,
  sentiment_score: Float?,
  sentiment_label: Enum["positive", "negative", "neutral"]?,
  created_at: Date,
  updated_at: Date
}
```

### User Feature Documents
```javascript
// Wishlist
{
  _id: ObjectId,
  user_id: ObjectId (ref: User),
  product_id: ObjectId (ref: Product),
  created_at: Date
}

// Price Alert
{
  _id: ObjectId,
  user_id: ObjectId (ref: User),
  product_id: ObjectId (ref: Product),
  target_price: Float,
  is_active: Boolean,
  created_at: Date,
  updated_at: Date,
  last_checked: Date?
}

// Search History
{
  _id: ObjectId,
  user_id: ObjectId (ref: User),
  query: String,
  results_count: Int,
  created_at: Date
}
```

## 🔑 API Authentication Endpoints

### Registration
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "date_of_birth": "1990-01-01"
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "date_of_birth": "1990-01-01",
  "role": "user",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-01T12:00:00Z",
  "last_login": null
}
```

### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username_or_email": "johndoe",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Get Current User Profile
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-01T12:00:00Z",
  "last_login": "2024-01-01T14:30:00Z",
  "preferences": {
    "preferred_categories": ["electronics", "clothing"],
    "preferred_brands": ["apple", "samsung"],
    "email_notifications": true,
    "push_notifications": true
  }
}
```

## 👤 User Feature Endpoints

### Wishlist Management
```http
# Add to wishlist
POST /api/v1/user/wishlist
Authorization: Bearer <access_token>
{
  "product_id": "507f1f77bcf86cd799439011"
}

# Get user's wishlist
GET /api/v1/user/wishlist
Authorization: Bearer <access_token>

# Remove from wishlist
DELETE /api/v1/user/wishlist/507f1f77bcf86cd799439011
Authorization: Bearer <access_token>
```

### Price Alerts
```http
# Create price alert
POST /api/v1/user/alerts
Authorization: Bearer <access_token>
{
  "product_id": "507f1f77bcf86cd799439011",
  "target_price": 99.99
}

# Get user's price alerts
GET /api/v1/user/alerts?active_only=true
Authorization: Bearer <access_token>

# Update price alert
PATCH /api/v1/user/alerts/507f1f77bcf86cd799439011
Authorization: Bearer <access_token>
{
  "target_price": 89.99,
  "is_active": true
}
```

### Search History
```http
# Get search history
GET /api/v1/user/search-history?limit=20
Authorization: Bearer <access_token>

# Clear search history
DELETE /api/v1/user/search-history
Authorization: Bearer <access_token>
```

### User Dashboard Statistics
```http
GET /api/v1/user/dashboard/stats
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "wishlist_count": 15,
  "active_alerts_count": 5,
  "search_history_count": 128,
  "recent_searches": [
    {
      "query": "iPhone 15",
      "results_count": 25,
      "created_at": "2024-01-01T14:30:00Z"
    }
  ]
}
```

## 🛍️ Enhanced Product Search

### Search with User Context
```http
GET /api/v1/products/search?query=smartphone&min_price=500&max_price=1000&category=electronics&limit=20
Authorization: Bearer <access_token> # Optional - for search history
```

**Features:**
- **Authenticated Users**: Search queries are automatically saved to search history
- **Personalization**: Future versions can use search history for recommendations
- **Filter Support**: Price range, category, platform, brand filtering
- **Sentiment Analysis**: Each product includes sentiment summary from reviews

## 🔒 Security Features

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter  
- At least one digit
- Bcrypt hashing with salt

### JWT Token Security
- **Access Token**: 30 minutes expiry (configurable)
- **Refresh Token**: 7 days expiry (configurable)
- **Algorithm**: HS256
- **Secret Key**: Configurable via environment

### Role-Based Access Control
- **USER**: Basic access to personal features
- **ADMIN**: Full system access, user management
- **MODERATOR**: Content moderation capabilities

### API Security
- **CORS**: Configurable allowed origins
- **Rate Limiting**: Built-in rate limiting middleware
- **Input Validation**: Comprehensive Pydantic validation
- **Error Handling**: Secure error responses without information leakage

## 🚀 Getting Started

### 1. Environment Setup
```bash
# Copy and configure environment variables
cp backend/.env.example backend/.env

# Update MongoDB connection and JWT secret
MONGODB_URL=mongodb://localhost:27017/smartshopper
SECRET_KEY=your-super-secret-key-here
```

### 2. Database Initialization
```bash
# Start MongoDB
docker-compose up -d mongodb

# The database will be automatically initialized with indexes
```

### 3. Start the Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 4. API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📱 Frontend Integration

### Authentication State Management
```javascript
// Store tokens securely
localStorage.setItem('access_token', response.access_token);
localStorage.setItem('refresh_token', response.refresh_token);

// Add to all API requests
const token = localStorage.getItem('access_token');
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}

// Handle token refresh
if (response.status === 401) {
  await refreshToken();
  // Retry original request
}
```

### User Context
```javascript
// Get current user on app load
const getCurrentUser = async () => {
  const response = await fetch('/api/v1/auth/me', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
};

// Check if user is authenticated
const isAuthenticated = () => {
  const token = localStorage.getItem('access_token');
  return token && !isTokenExpired(token);
};
```

## 🎯 Next Phase Features

### Phase 3: Advanced User Features
- [ ] **Social Features**: User reviews, follow users, share wishlists
- [ ] **Advanced Recommendations**: ML-based personalized product recommendations
- [ ] **Notification System**: Real-time price drop alerts, email notifications
- [ ] **User Analytics**: Purchase tracking, savings calculator
- [ ] **Multi-tenant Support**: Organization accounts, team wishlists

### Phase 4: AI & ML Integration
- [ ] **Smart Alerts**: Predictive price drop notifications
- [ ] **Personalized Search**: Search results ranked by user preferences
- [ ] **Review Intelligence**: Fake review detection, helpful review ranking
- [ ] **Chatbot Integration**: AI-powered shopping assistant

## 🔧 Configuration Options

### Environment Variables
```bash
# Core Settings
MONGODB_URL=mongodb://localhost:27017/smartshopper
SECRET_KEY=your-super-secret-key
DEBUG=true

# Token Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:3000"]

# External APIs
AMAZON_API_KEY=your-key
FLIPKART_API_KEY=your-key
```

### Database Indexes
The system automatically creates optimized indexes for:
- **Text Search**: Full-text search on products
- **User Lookups**: Username and email uniqueness
- **Query Performance**: Product categories, brands, prices
- **User Data**: Efficient wishlist, alert, and history queries

## 🆘 Troubleshooting

### Common Issues

**MongoDB Connection Failed**
```bash
# Check if MongoDB is running
docker-compose ps

# View MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

**Authentication Errors**
- Verify JWT secret key is consistent
- Check token expiration times
- Ensure proper Authorization header format: `Bearer <token>`

**Database Query Issues**
- Verify indexes are created properly
- Check MongoDB logs for query performance
- Use MongoDB Compass for database inspection

## 📈 Performance Considerations

### Database Optimization
- **Indexes**: All frequently queried fields are indexed
- **Aggregation**: Complex queries use MongoDB aggregation pipeline
- **Connection Pooling**: Async connections with proper pooling
- **Caching**: Redis integration ready for caching frequently accessed data

### API Performance
- **Async/Await**: Full async support throughout the application
- **Pagination**: All list endpoints support skip/limit pagination  
- **Field Selection**: Responses include only necessary fields
- **Batch Operations**: Support for bulk operations where applicable

---

This authentication system provides a solid foundation for SmartShopper's user management needs while maintaining security best practices and scalability for future enhancements.
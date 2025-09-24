// MongoDB initialization script for SmartShopper
db = db.getSiblingDB('smartshopper');

// Create application user
db.createUser({
  user: "smartshopper_user",
  pwd: "smartshopper_pass",
  roles: [
    {
      role: "readWrite",
      db: "smartshopper"
    }
  ]
});

// Create collections with initial indexes
db.createCollection("users");
db.createCollection("products");
db.createCollection("offers");
db.createCollection("reviews");
db.createCollection("price_alerts");
db.createCollection("wishlists");
db.createCollection("search_history");
db.createCollection("user_preferences");

// Create text index for product search
db.products.createIndex({ 
  "name": "text", 
  "description": "text", 
  "category": "text", 
  "brand": "text" 
});

// Create indexes for better query performance
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 }, { unique: true });
db.products.createIndex({ "category": 1 });
db.products.createIndex({ "brand": 1 });
db.offers.createIndex({ "product_id": 1 });
db.offers.createIndex({ "platform": 1 });
db.offers.createIndex({ "price": 1 });
db.reviews.createIndex({ "product_id": 1 });
db.reviews.createIndex({ "rating": 1 });
db.reviews.createIndex({ "sentiment_label": 1 });
db.price_alerts.createIndex({ "user_id": 1 });
db.price_alerts.createIndex({ "product_id": 1 });
db.price_alerts.createIndex({ "is_active": 1 });
db.wishlists.createIndex({ "user_id": 1 });
db.search_history.createIndex({ "user_id": 1 });
db.search_history.createIndex({ "created_at": -1 });

print("SmartShopper database initialized successfully!");
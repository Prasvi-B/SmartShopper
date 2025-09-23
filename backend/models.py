from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    canonical_title = Column(String)
    normalized_title = Column(String)
    slug = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    offers = relationship('Offer', back_populates='product')
    reviews = relationship('Review', back_populates='product')

class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    site = Column(String)
    price = Column(Float)
    currency = Column(String)
    url = Column(String)
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)
    product = relationship('Product', back_populates='offers')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    source = Column(String)
    text = Column(String)
    rating = Column(Float)
    predicted_sentiment = Column(String)
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)
    product = relationship('Product', back_populates='reviews')

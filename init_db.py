#!/usr/bin/env python3
"""
Database initialization script
Run this to create database tables manually
"""

from app import app, db
from models import CartItem, Feedback, Order

def init_database():
    """Initialize the database with all required tables"""
    with app.app_context():
        try:
            # Drop all tables (optional - only if you want to start fresh)
            # db.drop_all()
            
            # Create all tables
            db.create_all()
            
            print("✅ Database tables created successfully!")
            print("Tables created:")
            print("- cart_item")
            print("- feedback") 
            print("- order")
            
        except Exception as e:
            print(f"❌ Error creating database: {e}")

if __name__ == "__main__":
    init_database()
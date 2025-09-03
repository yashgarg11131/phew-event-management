from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    service_name = db.Column(db.String(100), nullable=False)
    service_price = db.Column(db.Float, nullable=False)
    service_description = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CartItem {self.service_name}>'

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Feedback {self.name} - {self.rating} stars>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    services = db.Column(db.Text, nullable=False)  # JSON string of services
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Order {self.customer_name} - ${self.total_amount}>'
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Mail, Message
from models import db, CartItem, Feedback, Order
from config import Config
import json
from datetime import datetime
import uuid
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
mail = Mail(app)

# Create database tables
def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {e}")

# Initialize database
init_db()

# Event packages data
EVENT_PACKAGES = {
    'birthday': {
        'name': 'Birthday Party Package',
        'price': 299.99,
        'description': 'Complete birthday celebration with decorations, cake, entertainment, and party favors.',
        'features': ['Custom decorations', 'Birthday cake', 'Entertainment', 'Party favors', 'Photography']
    },
    'baby_shower': {
        'name': 'Baby Shower Package',
        'price': 399.99,
        'description': 'Elegant baby shower setup with themed decorations, games, and refreshments.',
        'features': ['Themed decorations', 'Games & activities', 'Refreshments', 'Gift table setup', 'Photo booth']
    },
    'wedding': {
        'name': 'Wedding Ceremony Package',
        'price': 1999.99,
        'description': 'Comprehensive wedding package with venue decoration, catering, and coordination.',
        'features': ['Venue decoration', 'Catering service', 'Wedding coordination', 'Floral arrangements', 'Music & lighting']
    },
    'pre_wedding': {
        'name': 'Pre-Wedding Celebration',
        'price': 899.99,
        'description': 'Pre-wedding events including engagement party, sangeet, and mehendi ceremonies.',
        'features': ['Multiple event setup', 'Traditional decorations', 'Music & dance floor', 'Catering', 'Photography']
    },
    'corporate': {
        'name': 'Corporate Events Package',
        'price': 799.99,
        'description': 'Professional corporate event management for conferences, meetings, and team building.',
        'features': ['Professional setup', 'AV equipment', 'Catering service', 'Registration desk', 'Event coordination']
    },
    'house_party': {
        'name': 'House Party Package',
        'price': 199.99,
        'description': 'Intimate house party setup with music, lighting, and refreshments.',
        'features': ['Music system', 'Party lighting', 'Refreshments', 'Games & entertainment', 'Cleanup service']
    },
    'anniversary': {
        'name': 'Anniversary Celebration',
        'price': 599.99,
        'description': 'Romantic anniversary celebration with elegant decorations and dinner setup.',
        'features': ['Romantic decorations', 'Dinner setup', 'Floral arrangements', 'Candle lighting', 'Photography']
    }
}

# Service providers data
SERVICE_PROVIDERS = {
    'house_help': {
        'name': 'House Help Services',
        'price': 25.00,
        'unit': 'per hour',
        'description': 'Professional house help for event preparation, service, and assistance.',
        'features': ['Event setup assistance', 'Guest service', 'Kitchen help', 'General event support', 'Flexible hours']
    },
    'waiters': {
        'name': 'Professional Waiters',
        'price': 30.00,
        'unit': 'per hour',
        'description': 'Experienced waitstaff for seamless food and beverage service at your event.',
        'features': ['Professional service', 'Food & beverage serving', 'Table management', 'Guest assistance', 'Uniform provided']
    },
    'bartenders': {
        'name': 'Expert Bartenders',
        'price': 45.00,
        'unit': 'per hour',
        'description': 'Skilled bartenders to craft cocktails and manage your event bar service.',
        'features': ['Professional mixology', 'Bar setup & management', 'Custom cocktail menu', 'Equipment provided', 'TIPS certified']
    },
    'decorators': {
        'name': 'Event Decorators',
        'price': 150.00,
        'unit': 'per event',
        'description': 'Creative decorators to transform your venue with stunning visual designs.',
        'features': ['Custom decoration design', 'Theme development', 'Setup & installation', 'Quality materials', 'Cleanup included']
    },
    'musicians': {
        'name': 'Live Musicians',
        'price': 200.00,
        'unit': 'per event',
        'description': 'Talented musicians to provide live entertainment for your special occasion.',
        'features': ['Live music performance', 'Various music genres', 'Professional equipment', 'Custom playlist', 'Sound system included']
    },
    'cleaners': {
        'name': 'After Party Cleaners',
        'price': 120.00,
        'unit': 'per event',
        'description': 'Professional cleaning crew for post-event cleanup and venue restoration.',
        'features': ['Complete venue cleanup', 'Trash removal', 'Equipment breakdown', 'Venue restoration', 'Next-day service available']
    }
}

# Combined services for easy access
SERVICES = {**EVENT_PACKAGES, **SERVICE_PROVIDERS}

def get_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

@app.route('/')
def index():
    return render_template('index.html', 
                         event_packages=EVENT_PACKAGES, 
                         service_providers=SERVICE_PROVIDERS)

@app.route('/services')
def services():
    return render_template('services.html', 
                         event_packages=EVENT_PACKAGES, 
                         service_providers=SERVICE_PROVIDERS,
                         services=SERVICES)

@app.route('/add_to_cart/<service_key>')
def add_to_cart(service_key):
    if service_key not in SERVICES:
        flash('Service not found!', 'error')
        return redirect(url_for('services'))
    
    service = SERVICES[service_key]
    session_id = get_session_id()
    
    try:
        # Check if item already in cart
        existing_item = CartItem.query.filter_by(
            session_id=session_id, 
            service_name=service['name']
        ).first()
        
        if existing_item:
            flash('Item already in cart!', 'info')
        else:
            cart_item = CartItem(
                session_id=session_id,
                service_name=service['name'],
                service_price=service['price'],
                service_description=service['description']
            )
            db.session.add(cart_item)
            db.session.commit()
            flash('Added to cart successfully!', 'success')
    except Exception as e:
        # If database error, reinitialize
        init_db()
        flash('Database error. Please try again.', 'error')
    
    return redirect(url_for('services'))

@app.route('/cart')
def cart():
    session_id = get_session_id()
    try:
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
        total = sum(item.service_price for item in cart_items)
        return render_template('cart.html', cart_items=cart_items, total=total)
    except Exception as e:
        # If database error, reinitialize and return empty cart
        init_db()
        flash('Cart temporarily unavailable. Please try again.', 'info')
        return render_template('cart.html', cart_items=[], total=0)

@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    session_id = get_session_id()
    cart_item = CartItem.query.filter_by(id=item_id, session_id=session_id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart!', 'success')
    else:
        flash('Item not found!', 'error')
    
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    session_id = get_session_id()
    cart_items = CartItem.query.filter_by(session_id=session_id).all()
    
    if not cart_items:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('services'))
    
    if request.method == 'POST':
        # Get form data
        customer_name = request.form.get('name')
        customer_email = request.form.get('email')
        customer_phone = request.form.get('phone')
        event_date = request.form.get('event_date')
        
        # Validate data
        if not all([customer_name, customer_email, customer_phone, event_date]):
            flash('Please fill in all fields!', 'error')
            return render_template('checkout.html', cart_items=cart_items)
        
        # Calculate total
        total_amount = sum(item.service_price for item in cart_items)
        
        # Create order
        services_json = json.dumps([{
            'name': item.service_name,
            'price': item.service_price,
            'description': item.service_description
        } for item in cart_items])
        
        order = Order(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            event_date=datetime.strptime(event_date, '%Y-%m-%d').date(),
            total_amount=total_amount,
            services=services_json
        )
        
        db.session.add(order)
        
        # Clear cart
        CartItem.query.filter_by(session_id=session_id).delete()
        db.session.commit()
        
        # Send email confirmation
        send_confirmation_email(order)
        
        flash('Order placed successfully! Check your email for confirmation.', 'success')
        return redirect(url_for('index'))
    
    total = sum(item.service_price for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

def send_confirmation_email(order):
    try:
        services_data = json.loads(order.services)
        
        msg = Message(
            subject='Order Confirmation - Phew !! Event Management',
            recipients=[order.customer_email],
            html=render_template('email_confirmation.html', order=order, services=services_data)
        )
        
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        rating = request.form.get('rating')
        message = request.form.get('message')
        
        if not all([name, rating, message]):
            flash('Please fill in all fields!', 'error')
        else:
            feedback_entry = Feedback(
                name=name,
                rating=int(rating),
                message=message
            )
            db.session.add(feedback_entry)
            db.session.commit()
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('feedback'))
    
    # Get recent feedback to display
    recent_feedback = Feedback.query.order_by(Feedback.date_submitted.desc()).limit(10).all()
    return render_template('feedback.html', feedback_list=recent_feedback)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
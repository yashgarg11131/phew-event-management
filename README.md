# Phew! - Event Management Platform

A comprehensive Flask-based event management platform for organizing various events including birthdays, weddings, corporate events, and more.

## Features

- **Event Packages**: Complete event management packages for different occasions
- **Service Providers**: Individual service providers (bartenders, waiters, musicians, etc.)
- **Shopping Cart**: Add services to cart and checkout
- **Order Management**: Complete order processing with email confirmations
- **Feedback System**: Customer reviews and ratings
- **City Availability Checker**: Check if services are available in your city
- **Contact Form**: Interactive contact form with success popup
- **Responsive Design**: Mobile-friendly interface with custom branding

## Tech Stack

- **Backend**: Python Flask 2.3.3
- **Database**: SQLite with SQLAlchemy
- **Frontend**: HTML5, Tailwind CSS, Font Awesome icons
- **Email**: Flask-Mail for SMTP integration
- **Session Management**: Flask sessions for cart functionality

## Installation

1. **Clone/Download** the project to your local machine

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables** (Optional):
   Create a `.env` file for email configuration:
   ```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the Application**:
   Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
phew/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage
│   ├── services.html     # Services page
│   ├── cart.html         # Shopping cart
│   ├── checkout.html     # Checkout form
│   ├── feedback.html     # Customer feedback
│   ├── contact.html      # Contact information
│   └── email_confirmation.html  # Email template
├── static/
│   ├── css/             # Custom CSS files (if any)
│   ├── js/              # JavaScript files (if any)
│   └── images/          # Static images
└── instance/
    └── phew.db          # SQLite database (created automatically)
```

## Database Models

### CartItem
- Session-based cart items
- Service name, price, description
- Date added tracking

### Feedback
- Customer reviews and ratings
- Name, rating (1-5), message
- Submission timestamp

### Order
- Complete order information
- Customer details, event date
- Services purchased, total amount

## Email Configuration

To enable email confirmations:

1. **Gmail Setup** (Recommended):
   - Use Gmail SMTP settings
   - Generate an App Password for authentication
   - Update environment variables

2. **Other Email Providers**:
   - Update `MAIL_SERVER` and `MAIL_PORT` in config.py
   - Adjust TLS/SSL settings as needed

## Service Packages

The application includes 7 pre-defined event packages:

1. **Birthday Party Package** - $299.99
2. **Baby Shower Package** - $399.99
3. **Wedding Ceremony Package** - $1999.99
4. **Pre-Wedding Celebration** - $899.99
5. **Corporate Events Package** - $799.99
6. **House Party Package** - $199.99
7. **Anniversary Celebration** - $599.99

## Customization

### Adding New Services
1. Update the `SERVICES` dictionary in `app.py`
2. Add corresponding icons and styling in templates
3. Update service cards in `services.html`

### Theme Customization
- Primary colors are defined in the Tailwind config in `base.html`
- Yellow-based color scheme: primary, secondary, accent, dark
- Modify gradient backgrounds and color classes as needed

### Email Templates
- Customize `email_confirmation.html` for branded email design
- Update company information and styling

## Security Features

- Session-based cart (no sensitive data stored)
- CSRF protection through Flask's built-in features
- Email validation and sanitization
- Secure database queries using SQLAlchemy ORM

## Production Deployment

1. **Environment Variables**:
   - Set `SECRET_KEY` to a secure random string
   - Configure email settings
   - Set `DATABASE_URL` if using external database

2. **Database**:
   - Consider PostgreSQL for production
   - Update connection string in config.py

3. **Web Server**:
   - Use Gunicorn or uWSGI
   - Configure reverse proxy (Nginx)
   - Enable HTTPS

## Deployment

### Deploy to Render (Recommended)

1. **Create a Render account** at [render.com](https://render.com)

2. **Connect your GitHub repository**
   - Push this project to GitHub
   - Connect your GitHub account to Render

3. **Create a new Web Service**
   - Select your repository
   - Set the following:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Environment**: Python 3

4. **Set Environment Variables**:
   ```
   SECRET_KEY=your-super-secret-key-here
   DATABASE_URL=postgresql://... (Render provides this)
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=phew.org@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=phew.org@gmail.com
   ```

5. **Deploy**: Render will automatically deploy your app

### Deploy to Railway

1. **Create Railway account** at [railway.app](https://railway.app)
2. **Deploy from GitHub** - Railway auto-detects Flask
3. **Set Environment Variables** (same as above)
4. **One-click deploy**

### Deploy to Heroku

1. **Install Heroku CLI**
2. **Login and create app**:
   ```bash
   heroku login
   heroku create your-app-name
   ```
3. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set MAIL_USERNAME=phew.org@gmail.com
   heroku config:set MAIL_PASSWORD=your-app-password
   heroku config:set MAIL_DEFAULT_SENDER=phew.org@gmail.com
   ```
4. **Deploy**:
   ```bash
   git push heroku main
   ```

## Contact Information

- **Email**: phew.org@gmail.com
- **Phone**: 8789015663
- **Address**: Advant Navis Business Park, Sector 142, Greater Noida Expy, Uttar Pradesh, 201304

## License

This project is private and proprietary.
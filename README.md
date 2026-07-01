# EventHub

IFQ557 Assignment 2 - Event Management System

## Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

The app will be available at http://127.0.0.1:5000

## Project Structure

```
a3_group1/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .gitignore
└── eventhub/                # Application module
    ├── __init__.py          # Flask app factory + extension setup
    ├── models.py            # Database models (User, Event, Booking, Comment)
    ├── forms.py             # WTForms form definitions
    ├── views.py             # Main blueprint (landing page)
    ├── auth.py              # Auth blueprint (register, login, logout)
    ├── event.py             # Event blueprint (CRUD, comments)
    ├── booking.py           # Booking blueprint (book, history)
    ├── static/
    │   └── css/style.css    # Custom styles
    └── templates/
        ├── base.html        # Base template with navbar
        ├── index.html       # Landing page
        ├── user.html        # Login/register form
        ├── 404.html         # 404 error page
        ├── 500.html         # 500 error page
        ├── event/
        │   ├── list.html    # Event browsing
        │   ├── detail.html   # Event details
        │   ├── create.html   # Create event
        │   └── update.html   # Update event
        └── booking/
            ├── book.html     # Book tickets
            └── history.html  # Booking history
```

## Tech Stack

- Python 3 + Flask
- Flask-SQLAlchemy (ORM + SQLite)
- Flask-Login (session management)
- Flask-WTF / WTForms (form handling)
- Flask-Bcrypt (password hashing)
- Bootstrap-Flask (Bootstrap 5 integration)
- Bootstrap 5 (responsive UI)

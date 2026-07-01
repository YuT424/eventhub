from . import db
from datetime import datetime
from flask_login import UserMixin


# ============================================================
#  Event status constants
# ============================================================
class EventStatus:
    OPEN = "Open"
    INACTIVE = "Inactive"
    SOLD_OUT = "Sold Out"
    CANCELLED = "Cancelled"

    @classmethod
    def all(cls):
        return [cls.OPEN, cls.INACTIVE, cls.SOLD_OUT, cls.CANCELLED]


# ============================================================
#  User  -  user account + login credentials
# ============================================================
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)

    # relationships
    events = db.relationship("Event", backref="creator", lazy="dynamic")
    bookings = db.relationship("Booking", backref="user", lazy="dynamic")
    comments = db.relationship("Comment", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.id} {self.email}>"


# ============================================================
#  Event  -  event details + status management
# ============================================================
class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(64), nullable=False, index=True)
    date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    total_tickets = db.Column(db.Integer, nullable=False)
    available_tickets = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=EventStatus.OPEN)
    image = db.Column(db.String(500), nullable=True)

    # foreign key to creator
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationships
    bookings = db.relationship("Booking", backref="event", lazy="dynamic")
    comments = db.relationship("Comment", backref="event", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Event {self.id} {self.name}>"


# ============================================================
#  Booking  -  ticket purchase records + Order ID
# ============================================================
class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(36), unique=True, nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    def __repr__(self):
        return f"<Booking {self.id} order={self.order_id}>"


# ============================================================
#  Comment  -  user comments on events
# ============================================================
class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    def __repr__(self):
        return f"<Comment {self.id} by user={self.user_id}>"

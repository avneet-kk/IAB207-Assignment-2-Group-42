from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(160), nullable=False)
    total_tickets = db.Column(db.Integer, default=0, nullable=False)
    sold_tickets  = db.Column(db.Integer, default=0, nullable=False)
    is_cancelled  = db.Boolean,
    image_path    = db.Column(db.String(255))
    owner_id      = db.Column(db.Integer, db.ForeignKey('user.id'))

    # property
    def status(self):
        if self.is_cancelled: return "Cancelled"
        if self.date < datetime.now(): return "Inactive"
        if self.sold_tickets >= self.total_tickets: return "Sold Out"
        return "Open"

class Comment(db.Model):

class Order(db.Model): #Booking
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(40), unique=True, index=True, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event')

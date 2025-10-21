from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    surname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')

    def __repr__(self):
        return f"Name: {self.name}"


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
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event') 

class Order(db.Model): #Booking
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(40), unique=True, index=True, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event')

class Event:
    def __init__(self, name, description, date, venue, time, tickets, duration, price):
        self.name = name
        self.description = description
        self.date = date
        self.venue = venue
        self.time = time
        self.tickets = tickets
        self.duration = duration
       
    def set_feature_section(self, feature_section):
        self.set_feature_section.append(feature_section)

    def __repr__(self):
        return f"Name: {self.name}, Date: {self.date}, Venue: {self.venue}, Time: {self.time}, Tickets: {self.tickets}, Duration {self.duration}"


class Feature_section: 
    def __init__(self,hit_songs, visual_spectacle, fan_interaction):
        self.hit_songs = hit_songs
        self.visual_spectacle = visual_spectacle
        self.fan_interaction = fan_interaction

    def __repr__(self):
        return f"Hit Songs {self.hit_songs}, \n Visual Spectacle {self.visual_spectacle}, \n Fan Interaction {self.fan_interaction}"


from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(20))
    street_address = db.Column(db.String(200))
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')
    #events = db.relationship('Event', backref='user') for tracking creator of each event (remember you would have to reset the database for this)

    def set_password(self, password):
        """Hashes password before storing"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Validates input password against stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.first_name} {self.surname}>"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time=db.Column(db.Time, nullable=False)
    location = db.Column(db.String(160), nullable=False)
    total_tickets = db.Column(db.Integer, default=0, nullable=False)
    sold_tickets  = db.Column(db.Integer, default=0, nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)
    # is_cancelled  = db.Column(db.Boolean, default=False)
    is_cancelled  = db.Column(db.Boolean, default=False)
    image_path    = db.Column(db.String(255))
    owner_id      = db.Column(db.Integer, db.ForeignKey('user.id'))

    # property
    def status(self):
        if self.is_cancelled: return "Cancelled"
        if self.date < datetime.now(): return "Inactive"
        if self.sold_tickets >= self.total_tickets: return "Sold Out"
        return "Open"
    
    # # passing data 
    # def __init__(self, name description, image, category, date, location, total_tickets):
    #     self.name = name 
    #     self.description = description 
    #     self.image = image 
    #     self.category = category 
    #     self.date = date 
    #     self.location = location 
    #     self.total_tickets = total_tickets 
    
    # def __repr__(): 
    #     return f"Name: {self.name}, Description: {self.description}, Date: {self.date}, Location: {self.location}"


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
    event = db.relationship('Event', lazy=True)


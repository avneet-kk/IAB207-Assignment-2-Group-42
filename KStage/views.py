from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_required, current_user, LoginManager
from . import db
from .models import Event, Order
from .forms import RegisterForm, LoginForm, BookingForm, EventForm
import secrets
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing page."""
    # If you prefer to route visitors straight to events, use:
    # return redirect(url_for('main.events'))
    return render_template('index.html')

@main_bp.route('/events')
def events():
    """List all events from the database."""
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template('events.html', events=events)

@main_bp.route('/events/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id: int):
    """Show one event and handle booking form submission."""
    event = Event.query.get_or_404(event_id)
    form = BookingForm()

    if form.validate_on_submit():
        # Booking requires authentication
        if not current_user.is_authenticated:
            # Send the user to login and come back here after login
            return redirect(url_for('auth.login', next=request.path))

        # Validate business rules: status must be Open
        if event.status != "Open":
            flash(f'Booking not allowed: {event.status}', 'warning')
            return redirect(request.path)

        qty = form.qty.data
        remaining = event.total_tickets - event.sold_tickets
        if qty > remaining:
            flash(f'{remaining} tickets left', 'warning')
            return redirect(request.path)

        # Create an order with a short human-friendly reference
        order_id = "K-" + secrets.token_hex(4).upper()
        db.session.add(Order(order_id=order_id, qty=qty,
                             user_id=current_user.id, event_id=event.id))
        event.sold_tickets += qty
        db.session.commit()

        flash(f'Booked! Order ID: {order_id}', 'success')
        return redirect(url_for('main.booking_history'))

    # GET or invalid POST -> render page with form + event details
    return render_template('event-details.html', event=event, form=form)

@main_bp.route('/create_events', methods=['GET', 'POST'])
def create_events():
    """Create a new event and save it to the database."""
    form = EventForm()

    if form.validate_on_submit():
        new_event = Event(
            title=form.title.data.strip(),
            category=form.category.data,
            description=form.description.data.strip(),
            date=form.date.data,
            location=form.location.data.strip(),
            total_tickets=form.total_tickets.data,
            image_path=form.image_path.data or None,
            owner_id=current_user.id,
            sold_tickets=0,
            is_cancelled=False,
        )
        db.session.add(new_event)
        db.session.commit()

        flash("Event created succesfully!", "success")
        return redirect(url_for('main.events'))
    
    return render_template('create-event.html', form=form)

@main_bp.route('/bookings')
@login_required
def booking_history():
    """Show the logged-in user's bookings (most recent first)."""
    bookings = (Order.query
                .filter_by(user_id=current_user.id)
                .order_by(Order.created_at.desc())
                .all())
    return render_template('booking-history.html', bookings=bookings)

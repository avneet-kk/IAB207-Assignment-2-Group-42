from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_required, current_user, LoginManager
from . import db
from .models import Event, Order, Comment
from .forms import RegisterForm, LoginForm, BookingForm, EventForm, CommentForm
import secrets
from datetime import datetime
import os
from werkzeug.utils import secure_filename

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
    comment_form = CommentForm()

    if form.validate_on_submit():
        # Booking requires authentication
        if not current_user.is_authenticated:
            # Send the user to login and come back here after login
            return redirect(url_for('auth.login', next=request.path))

        # Validate business rules: status must be Open
        if event.status() != "Open":
            flash(f'Booking not allowed: {event.status()}', 'warning')
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

    # For GET or invalid POST, render the page with both forms
    # If Event.comments is lazy='dynamic', you can order here:
    comments = event.comments.order_by(Comment.created_at.desc()).all()  # newest first
    return render_template('event-details.html', event=event, form=form,
                           comment_form=comment_form, comments=comments)


@main_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    """Create a new event and save it to the database."""
    form = EventForm()

    if form.validate_on_submit():
        # Handle file upload
        image_file = form.image_path.data
        if image_file:
            # Get the filename and secure it
            filename = secure_filename(image_file.filename)
            # Get the base path (parent directory of KStage)
            BASE_PATH = os.path.dirname(os.path.dirname(__file__))
            # Create the upload directory if it doesn't exist
            upload_dir = os.path.join(BASE_PATH, 'KStage', 'static', 'img')
            os.makedirs(upload_dir, exist_ok=True)
            # Full path to save the file
            upload_path = os.path.join(upload_dir, filename)
            # Save the file
            image_file.save(upload_path)
            # Store relative path for database (relative to static folder)
            db_image_path = f'img/{filename}'
        else:
            db_image_path = None
        
        new_event = Event(
            title=form.title.data.strip(),
            category=form.category.data,
            description=form.description.data.strip(),
            date=form.date.data,
            time=form.time.data,
            location=form.location.data.strip(),
            total_tickets=form.total_tickets.data,
            ticket_price=form.price.data,
            image_path=db_image_path,
            owner_id=current_user.id,
            sold_tickets=0,
            is_cancelled=False,
        )
        db.session.add(new_event)
        db.session.commit()

        flash("Event created successfully!", "success")
        return redirect(url_for('main.events'))
    
    # Display form errors if validation failed
    if request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    
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


@main_bp.post('/events/<int:event_id>/comment')
@login_required
def add_comment(event_id: int):
    """
    Handle comment submission for an event.
    """
    event = Event.query.get_or_404(event_id)
    form = CommentForm()

    if form.validate_on_submit():
        c = Comment(
            content=form.comment.data.strip(),
            user_id=current_user.id,
            event_id=event.id
        )
        db.session.add(c)
        db.session.commit()
        flash("Comment posted!", "success")
    else:
        # show the first validation error(s)
        for field, errs in form.errors.items():
            for err in errs:
                flash(f"{field}: {err}", "danger")

    return redirect(url_for('main.event_detail', event_id=event.id))

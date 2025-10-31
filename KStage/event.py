from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event 
from .forms import EventForm
from . import db
from datetime import datetime

event_destbp = Blueprint('event', __name__, url_prefix='/event')

@event_destbp.route ('/<id>') 
def show (id):
    Event = db.session.scalar(db.select(Event).where(Event.id==id))
    # Event = get_event ()
    return render_template ('event/show.html', event = Event)

@event_destbp.route('/create_events', methods = ['GET', 'POST'])
def create_events():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():

    #combine date and time
    combined_datetime = datetime.combine(form.date.data, form.time.data)

    event = Event(title=form.title.data, 
                  category=form.category.data,
                  description=form.description.data,
                  date_time=combined_datetime,
                  location=form.location.data, 
                  total_tickets=int(form.total_tickets.data),
                  # owner_id=current_user.id,
                  image_path=form.image_path.data,
    )
    
    #add event to the database 
    db.session.add(event)
    #commit on the database
    db.session.commit()
    # print('Successfully created new event')

    # flash(f'Event "{event.title}" created successfully!', 'success')   

    # return redirect(url_for('events'))
  return render_template('destination/create.html', form=form)
  # Redirect to the event's detail page after successful creation
  # return redirect(url_for('main.event_detail', event_id=new_event.id))

#  def get_event():
    #create description of BTS fan signing event
    #b_desc = """"Get ready for the ultimate ARMY experience! Join us for an unforgettable BTS Fan Signing Event, where you’ll have the rare opportunity to meet your favorite members of BTS up close. This exclusive event brings fans together to celebrate love, music, and connection — the true essence of BTS. """
   
    #event = Event ('BTS fan sign', b_desc, 'Thursday, 9th October 2025', '7:00pm', 'Starting from $2000', 'Approx. 3 hours')

    #feature_section = feature_section("Experience all of TWICE's biggest hits including 'TT', 'Likey', 'What Is Love', and tracks from their latest albums.", "State-of-the-art lighting, LED screens, and stunning stage effects that create an immersive concert experience.", 'Special moments with ONCE, fan chants, and exclusive merchandise available only at the concert venue.')
    #feature_section = feature_section("Sam", "Visited during the olympics, was great", '2023-08-12 11:00:00')
    
    
    #event.set_feature_section(feature_section)
    #feature_section = feature_section("Bill", "free food!", '2023-08-12 11:00:00')
    #event.set_feature_section(feature_section)
    #feature_section = feature_section("Sally", "free face masks!", '2023-08-12 11:00:00')
    #event.set_feature_section(feature_section)
    


  # class Event(db.Model):
  #   id = db.Column(db.Integer, primary_key=True)
  #   title = db.Column(db.String(160), nullable=False)
  #   category = db.Column(db.String(80), nullable=False)
  #   description = db.Column(db.Text, nullable=False)
  #   date = db.Column(db.DateTime, nullable=False)
  #   location = db.Column(db.String(160), nullable=False)
  #   total_tickets = db.Column(db.Integer, default=0, nullable=False)
  #   sold_tickets  = db.Column(db.Integer, default=0, nullable=False)
  #   is_cancelled  = db.Boolean,
  #   image_path    = db.Column(db.String(255))
  #   owner_id      = db.Column(db.Integer, db.ForeignKey('user.id'))

    # return Event

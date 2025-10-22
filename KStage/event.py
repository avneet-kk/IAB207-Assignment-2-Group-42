from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event 
from .forms import EventForm

event_destbp = Blueprint('event', __name__, url_prefix='/event')

@event_destbp.route ('/<id>')
def show (id):
    Events = get_event ()
    return render_template ('event/show.html', event = Event)

@event_destbp.route('/create', methods = ['GET', 'POST'])
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    print('Successfully created new event')
    return redirect(url_for('event.create'))
  return render_template('destination/create.html', form=form)

def get_event():
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
    
    return "event"

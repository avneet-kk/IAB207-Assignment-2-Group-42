from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event 
from .forms import EventForm
from flask_login import login_required, current_user
from . import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

event_destbp = Blueprint('event', __name__, url_prefix='/event')
print('blueprint completed')
@event_destbp.route ('/<id>') 
def show (id):
    Event = db.session.scalar(db.select(Event).where(Event.id==id))
    print('connection sucessful')

    # Event = get_event ()
    return render_template ('destination/show.html', event = Event)

@event_destbp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  print('passed section A')
  if form.validate_on_submit():

    event = Event(title=form.title.data, 
                  category=form.category.data,
                  description=form.description.data,
                  date=form.date.data,
                  time=form.time.data,
                  location=form.location.data, 
                  total_tickets=int(form.total_tickets.data),
                  ticket_price=form.price.data,
                  owner_id=current_user.id,
                  image_path=form.image_path.data,
    )
    
    #add event to the database 
    db.session.add(event)
    #commit on the database
    db.session.commit()
    # print('Successfully created new event')

    flash(f'Event "{event.title}" created successfully!', 'success')   

    return redirect(url_for('event.show', id=event.id))
  
  elif request.method == 'POST':
        print('Form Validation Failed. Errors:')
        print(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')

  return render_template('destination/create.html', form=form)
print('created event')


def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  # save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

  

    # return redirect(url_for('events'))
  
  # Redirect to the event's detail page after successful creation
  # return redirect(url_for('main.event_detail', event_id=new_event.id))

def get_event():
    title = """BTS 6th World Tour"""
    category = """Concert"""
    description="""It's that time of year ARMY's... BTS is back with another World Tour!"""
    date='30th October, 2025 | 7:00pm'
    location="""Suncorp Stadium"""
    total_tickets='8000'
    ticket_price='1500'
    image_path='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFyC8pBJI2AAHLpAVih41_yWx2xxLleTtdshAdk1HOZQd9ZM8-Ag'
    return Event

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



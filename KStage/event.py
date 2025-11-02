from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event 
from .forms import EventForm
from flask_login import login_required, current_user
from . import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

event_destbp = Blueprint('event', __name__, url_prefix='/event')

@event_destbp.route('/create', methods = ['GET', 'POST'])
# @login_required
def createbp():
  print('Method type: ', request.method)
  form = EventForm()
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

@event_destbp.route ('/<id>') 
def show (id):
    Event = db.session.scalar(db.select(Event).where(Event.id==id))
    # Event = get_event ()
    return render_template ('destination/show.html', event = Event)

#function to upload file
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

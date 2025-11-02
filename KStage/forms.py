from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, SelectField, DateField, TimeField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, DataRequired
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}


# creates the login information
class LoginForm(FlaskForm):
    email =StringField("Email", validators=[InputRequired(), Email()])
    password=PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone_number =StringField("Phone Number", validators=[Length(max=12)])
    street_address =StringField("Street Address", validators=[Length(max=200)])
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password", message="Passwords should match")])
    # submit button
    submit = SubmitField("Register")

# for booking numbers
class BookingForm(FlaskForm):
    qty = IntegerField("Tickets", validators=[DataRequired(), NumberRange(min=1, max=1000)])
    submit = SubmitField("Book Now")

# for creating events
class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[InputRequired(), Length(max=200)])
    # Category dropdown box
    category = SelectField(
        'Category',
        choices=[
            ('concert', 'Concert'),
            ('fanmeeting', 'Fan Meeting'),
            ('dance', 'Dance Competition'),
            ('multigroup', 'Multi-Group'),
        ],
        validators=[InputRequired()]
    )
    date = DateField('Date', validators=[InputRequired()])
    time = TimeField('Time', validators=[InputRequired()])
    location = StringField('Venue', validators=[InputRequired()])
    price = IntegerField('Ticket Price', validators=[InputRequired(), NumberRange(min=0)])
    total_tickets = IntegerField('Tickets Available', validators=[InputRequired(), NumberRange(min=1)])
    image_path = FileField('Event Image', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    description = TextAreaField('Description', validators = [InputRequired()])

    #submit button
    submit = SubmitField('Create Event')

# for editing events
class EditEventForm(FlaskForm):
    title = StringField('Event Title', validators=[InputRequired(), Length(max=200)])
    # Category dropdown box
    category = SelectField(
        'Category',
        choices=[
            ('concert', 'Concert'),
            ('fanmeeting', 'Fan Meeting'),
            ('dance', 'Dance Competition'),
            ('multigroup', 'Multi-Group'),
        ],
        validators=[InputRequired()]
    )
    date = DateField('Date', validators=[InputRequired()])
    time = TimeField('Time', validators=[InputRequired()])
    location = StringField('Venue', validators=[InputRequired()])
    price = IntegerField('Ticket Price', validators=[InputRequired(), NumberRange(min=0)])
    total_tickets = IntegerField('Tickets Available', validators=[InputRequired(), NumberRange(min=1)])
    status = SelectField(
        'Event Status',
        choices=[
            ('Open', 'Open'),
            ('Cancelled', 'Cancelled'),
            ('Inactive', 'Inactive (Event in the past)'),
            ('Sold Out', 'Sold Out'),
        ],
        validators=[InputRequired()]
    )
    image_path = FileField('Event Image (leave empty to keep current image)', validators=[
        FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    description = TextAreaField('Description', validators = [InputRequired()])

    #submit button
    submit = SubmitField('Update Event')

#for comments
class CommentForm(FlaskForm):
    comment = TextAreaField("Add a Comment", validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField("Post Comment")

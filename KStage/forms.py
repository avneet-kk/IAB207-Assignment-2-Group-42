from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, SelectField, DateField, TimeField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange


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
    phone_number =StringField("Phone Number", validators=[Length(max=10)])
    street_address =StringField("Street Addres", validators=[Length(max=200)])
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password", message="Passwords should match")]),
    # submit button
    submit = SubmitField("Register")

# for booking numbers
class BookingForm(FlaskForm):
    qty = IntegerField("Tickets", validators=[InputRequired(), NumberRange(min=1)])
    submit = SubmitField("Book Now")

# for creating events
class EventForm(FlaskForm):
    name = StringField('Event Title', validators=[InputRequired()])
    # Category dropdown box
    category = SelectField(
        'Category',
        choices=[
            ('consert'),
            ('Fan Meeting'),
            ('Dance Competition'),
            ('Multi-Group '),
        ],
    )
    date = DateField('date', validators=[InputRequired()])
    time = TimeField('time', validators=[InputRequired()])
    location = StringField('Venue', validators=[InputRequired()])
    price = StringField('Ticket Price', validators=[InputRequired()])
    available = StringField('Ticket Available', validators=[InputRequired()])
    image = StringField('Event Image', validators=[InputRequired()])
    description = TextAreaField('Description', validators = [InputRequired()])

    #submit button
    submit = SubmitField('Create Event')

#for comments

class CommentForm(FlaskForm):
    comment = TextAreaField("Add a Comment", validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField("Post Comment")
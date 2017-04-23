
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, DateField
from models import db, User

class ContactForm(Form):
    name = TextField("Name", [validators.Required("Please enter a name")])
    email = TextField("Email", [validators.Required("Please enter a email"), validators.Email("Please enter a valid email")])
    phone = TextField("Phone", [validators.Required("Please enter a phone number")])
    subject = TextField("Subject", [validators.Required("Please enter a subject")])
    message = TextAreaField("Message", [validators.Required("Please enter a message")])
    submit = SubmitField("Send")
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    
    def validate(self):
        if not Form.validate(self):            
            return False
 
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")            
            return False
        else:
            return True
    
class CheckoutForm(Form):
    suiteId = TextField("suidId", [validators.Required("Please enter a suit ID")])    
    email = TextField("Email", [validators.Required("Please enter a email"), validators.Email("Please enter a valid email")])
    submit = SubmitField("Checkout")

class CheckinForm(Form):
    suiteId = TextField("suidId", [validators.Required("Please enter a suit ID")])    
    submit = SubmitField("Checkout")


class SignupForm(Form):    
    username = TextField("Username",  [validators.Required("Please enter your preferred username.")])
    fullname = TextField("Full name",  [validators.Required("Please enter your full name.")])    
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter a valid email address.")])
    uin = TextField("UIN",  [validators.Required("Please enter your UIN.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Create account")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    
    def validate(self):
        if not Form.validate(self):            
            return False
 
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")            
            return False
        else:
            return True
        
class SigninForm(Form):    
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter a valid email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")
     
    def __init__(self, *args, **kwargs):        
        Form.__init__(self, *args, **kwargs)
    
    def validate(self):
        if not Form.validate(self):
            return False
       
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False
        
class AvailabilityForm(Form):
    gender = TextField('Gender', [validators.Required("Please enter a gender.")])
    type = TextField('Type', [validators.Required("Please enter a suit type.")])
    submit = SubmitField("Search Availability")

class AppointmentForm():
    preference = TextField("Preference")
    date_val = DateField("date_val", [validators.Required("Please enter a date.")])
    time_val = DateField("time_val", [validators.Required("Please enter a time.")])
    submit = SubmitField("Schedule Appointment")
    

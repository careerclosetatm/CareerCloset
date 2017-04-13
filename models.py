
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "tbl_users"
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    fullname = db.Column(db.String(100))    
    email = db.Column(db.String(120), unique=True)
    uin = db.Column(db.String(10))
    pwdhash = db.Column(db.String(54))
   
    def __init__(self, username, fullname, email, uin, password):
        self.username = username.title()        
        self.fullname = fullname.title()
        self.email = email.lower()
        self.uin = uin.title()
        self.set_password(password)
         
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    
class Suits(db.Model):
    __tablename__ = "tbl_suits"
    suit_id = db.Column(db.String(100),primary_key=True)
    gender = db.Column(db.String(10))
    size = db.Column(db.String(100))
    type = db.Column(db.String(100))
    available = db.Column(db.Boolean, default=True)
    
    def __init__(self, suit_id, gender, size, type,available):
        self.suit_id = suit_id
        self.gender = gender
        self.type = type
        self.size = size
        self.available = available

class Order(db.Model):
    __tablename__ = "tbl_order"
    order_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    appointment_id = db.Column(db.Integer)
    suit_id = db.Column(db.Integer)
    returned = db.Column(db.Boolean)
    checkin_date = db.Column(db.Date)
    checkout_date = db.Column(db.Date)    
   
    def __init__(self, order_id, user_id, appointment_id, suit_id, returned, checkin_date, checkout_date):
        self.order_id = order_id.title()
        self.user_id = user_id.title()
        self.appointment_id = appointment_id.title()        
        self.suit_id = suit_id.title()
        self.returned = returned.title()
        self.checkin_date = checkin_date.title()
        self.checkout_date = checkout_date.title()
        
class Appointment(db.Model):
    __tablename__ = "tbl_appointment"
    appointment_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    time = db.Column(db.String(100))
   
    def __init__(self, appointment_id, user_id, date, time):
        self.appointment_id = appointment_id.title()
        self.user_id = user_id.title()
        self.date = date.title()        
        self.time = time.title()

        
class Schedule(db.Model):
    __tablename__ = "tbl_schedule"
    date_Value = db.Column(db.Date, primary_key = True)
    time9_00 = db.Column(db.Boolean)
    time9_30 = db.Column(db.Boolean)
    time10_00 = db.Column(db.Boolean)
    time10_30 = db.Column(db.Boolean)
    time11_00 = db.Column(db.Boolean)
    time11_30 = db.Column(db.Boolean)
    time12_00 = db.Column(db.Boolean)
    time12_30 = db.Column(db.Boolean)
    time13_00 = db.Column(db.Boolean)
    time13_30 = db.Column(db.Boolean)
    time14_00 = db.Column(db.Boolean)
    time14_30 = db.Column(db.Boolean)
    time15_00 = db.Column(db.Boolean)
    time15_30 = db.Column(db.Boolean)
    time16_00 = db.Column(db.Boolean)
    time16_30 = db.Column(db.Boolean)
    time17_00 = db.Column(db.Boolean)
    
    
    def __init__(self, date_Value, time9_00,time9_30,time10_00,time10_30,time11_00,time11_30,time12_00,time12_30,time13_00,time13_30,time14_00,time14_30,time15_00,time15_30,time16_00,time16_30,time17_00):
        self.date_Value = datetime.strptime (date_Value,'%Y-%m-%d')
        self.time9_00  = time9_00
        self.time9_30  = time9_30
        self.time10_00 = time10_00
        self.time10_30 = time10_30
        self.time11_00 = time11_00
        self.time11_30 = time11_30
        self.time12_00 = time12_00
        self.time12_30 = time12_30
        self.time13_00 = time13_00
        self.time13_30 = time13_30
        self.time14_00 = time14_00
        self.time14_30 = time14_30
        self.time15_00 = time15_00       
        self.time15_30 = time15_30
        self.time16_00 = time16_00
        self.time16_30 = time16_30
        self.time17_00 = time17_00
        
    def serialize(self):  
        return {           
            'date_Value': self.date_Value, 
            'time9_00': self.time9_00,
            'time9_30': self.time9_30,
            'time10_00': self.time10_00,
            'time10_30': self.time10_30,
            'time11_00': self.time11_00,
            'time11_30': self.time11_30,
            'time12_00': self.time12_00,
            'time12_30': self.time12_30,
            'time13_00': self.time13_00,
            'time13_30': self.time13_30,
            'time14_00': self.time14_00,
            'time14_30': self.time14_30,
            'time15_00': self.time15_00,
            'time15_30': self.time15_30,
            'time16_00': self.time16_00,
            'time16_30': self.time16_30,
            'time17_00': self.time17_00,
        }

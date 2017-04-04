
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
        
class Schedule(db.Model):
    __tablename__ = "tbl_schedule"
    date = db.Column(db.Date, primary_key = True)
    time9_00 = db.Column(db.Boolean)
    #time10_00 = db.Column(db.Boolean)
#     time11_00 = db.Column(db.Boolean)
#     time12_00 = db.Column(db.Boolean)
#     time1_00 = db.Column(db.Boolean)
#     time2_00 = db.Column(db.Boolean)
#     time3_00 = db.Column(db.Boolean)
#     time4_00 = db.Column(db.Boolean)
#     time5_00 = db.Column(db.Boolean)
    time10_00 = db.Column(db.Boolean)
    time11_00 = db.Column(db.Boolean)
    time12_00 = db.Column(db.Boolean)
    time1_00 = db.Column(db.Boolean)
    time2_00 = db.Column(db.Boolean)
    time3_00 = db.Column(db.Boolean)
    time4_00 = db.Column(db.Boolean)
    time5_00 = db.Column(db.Boolean)
    
    
    def __init__(self, date, time9_00, time10_00, time11_00, time12_00, time1_00, time2_00, time3_00, time4_00, time5_00):
        self.date = date
        self.time9_00 = time9_00.title()
        self.time10_00 = time10_00.title()
        self.time11_00 = time11_00.title()
        self.time12_00 = time12_00.title()
        self.time1_00 = time1_00.title()
        self.time2_00 = time2_00.title()
        self.time3_00 = time3_00.title()
        self.time4_00 = time4_00.title()
        self.time5_00 = time5_00.title()
        
    def serialize(self):  
        return {           
            #'date': self.date, 
            'time9_00': self.time9_00,
            'time10_00': self.time10_00,
            'time11_00': self.time11_00,
            'time12_00': self.time12_00,
            'time1_00': self.time1_00,
            'time2_00': self.time2_00,
            'time3_00': self.time3_00,
            'time4_00': self.time4_00,
            'time5_00': self.time5_00
        }
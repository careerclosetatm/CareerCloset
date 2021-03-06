
from flask import Flask, render_template, flash, request, session, url_for, redirect, jsonify
from forms import ContactForm, SignupForm, SigninForm, AvailabilityForm, CheckoutForm,AppointmentForm, CheckinForm
from flask_mail import Message, Mail
from models import db, User, Suits, Schedule, Appointment
from sqlalchemy import or_, and_, engine, table
from datetime import datetime, timedelta
import os

mail = Mail()

app = Flask(__name__)

@app.route("/")



def home():
    """Renders a template to take the user to the home screen.
    """    
    if "email" in session:        
        user = User.query.filter_by(email = session["email"]).first()
        if user is None:
            return redirect(url_for("signin"))        
    return render_template("home.html")

@app.route("/donate")
def donate():
    """Renders a template to take the user to the Donate Screen.
    """ 
    return render_template("donate.html")

@app.route("/dashboard0", methods=["GET", "POST"])
def dashboard0():
    """Renders a template to take the user to the Dash board Screen. 
     If the user is not logged in as admin, takes the user to the sign in screen.
     Also, updates the database with the suit that has been checked out.
    """ 
    if "email" not in session:
        session['path'] = request.url
        return redirect(url_for("signin"))
    user = User.query.filter_by(email = session["email"]).first()
    #print(user)
    if user is None:
        session['path'] = request.url
        return redirect(url_for("signin"))
    elif user.email =="careerclosetatm@gmail.com":
        form1 = CheckoutForm()
        form2 = CheckinForm()
        if request.method == "POST":
            print "inside post"
            print request.form["checkoutButtonClicked"]
            print request.form["checkinButtonClicked"]
            if form1.submit.data:
                # do some listing...
                print "checkout"
                if form1.validate() == False:
                    flash("All fields are required")
                    return render_template("dashboard0.html", form1=form1)
                else:
                    suits = Suits.query.filter(Suits.suit_id == form1.suiteId.data.upper()).first()                
                    if suits != None:
                        suits.available = False
                        db.session.commit()  
                        checkoutDate = datetime.now().date()
                        #checkoutDate = datetime.strptime(checkoutDateVal,"%m/%d/%y")
                        returnDate = checkoutDate + timedelta(days=5)                                                        
                        msg = Message("Confirmation of suit checkout",
                                  sender='careerclosetatm@gmail.com',
                                  recipients=[form1.email.data])
                        msg.body = """
                            From: Team Career Closet <%s>,
                            Howdy, 
                            This is a confirmation of your suit %s checkout on %s.
                            Please return the suit before the deadline %s
                            Gigem.
                            Team Career Closet.
                            """ % ('careerclosetatm@gmail.com',form1.suiteId.data.upper(),checkoutDate,returnDate)
                        mail.send(msg) 
                        
                    suits1 = Suits.query.filter(Suits.available==True).all()
                    suits2 = Suits.query.filter(Suits.available==False).all()
                    return render_template("dashboard0.html", success = "checkout-success", form1=form1, form2=form2, suits1=suits1, suits2=suits2)
            elif form2.submit.data:
                print "checkin"
                if form2.validate() == False:
                    flash("All fields are required")
                    return render_template("checkin.html", form2=form2)
                else:
                    suits = Suits.query.filter(Suits.suit_id == form2.suiteId.data.upper()).first()                
                    if suits != None:
                        suits.available = True
                        db.session.commit()  
                        checkinDate = datetime.now().date()
                        
                    #suits = Suits.query.filter(Suits.available==False).all()
                    suits1 = Suits.query.filter(Suits.available==True).all()
                    suits2 = Suits.query.filter(Suits.available==False).all()
                    #return render_template("checkin.html", success = True, form2=form2, suits=suits)
                    return render_template("dashboard0.html", success = "checkin-success", form1=form1, form2=form2, suits1=suits1, suits2=suits2)
                # do something else
            
        elif request.method == "GET":
            #suits = Suits.query.filter(Suits.available==True).all()
            suits1 = Suits.query.filter(Suits.available==True).all()
            suits2 = Suits.query.filter(Suits.available==False).all()                               
            #return render_template("dashboard0.html", form=form, suits=suits)
            return render_template("dashboard0.html", form1=form1, form2=form2, suits1=suits1, suits2=suits2)  
    else:
        return render_template("home.html")  
@app.route("/dashboard1", methods=["GET", "POST"]) 
   
def dashboard1():
    """Renders a template to take the user to the Dash board Screen for the check in functionality. 
     If the user is not logged in as admin, takes the user to the sign in screen.
    """    
    if "email" not in session:
        session['path'] = request.url
        return redirect(url_for("signin"))
    user = User.query.filter_by(email = session["email"]).first()
    #print(user)
    if user is None:
        session['path'] = request.url
        return redirect(url_for("signin"))
    elif user.email =="careerclosetatm@gmail.com":
        form1 = CheckoutForm()
        form2 = CheckinForm()
        if request.method == "POST":
            print "inside post1"
            print "checkin"
            if form2.validate() == False:
                flash("All fields are required")
                return render_template("checkin.html", form2=form2)
            else:
                suits = Suits.query.filter(Suits.suit_id == form2.suiteId.data.upper()).first()                
                if suits != None:
                    suits.available = True
                    db.session.commit()  
                    checkinDate = datetime.now().date()
                    
                #suits = Suits.query.filter(Suits.available==False).all()
                suits1 = Suits.query.filter(Suits.available==True).all()
                suits2 = Suits.query.filter(Suits.available==False).all()
                #return render_template("checkin.html", success = True, form2=form2, suits=suits)
                return render_template("dashboard0.html", success = "checkin-success", form1=form1, form2=form2, suits1=suits1, suits2=suits2)
                # do something else
            
        elif request.method == "GET":
            #suits = Suits.query.filter(Suits.available==True).all()
            suits1 = Suits.query.filter(Suits.available==True).all()
            suits2 = Suits.query.filter(Suits.available==False).all()                               
            #return render_template("dashboard0.html", form=form, suits=suits)
            return render_template("dashboard0.html", form1=form1, form2=form2, suits1=suits1, suits2=suits2)  
    else:
        return render_template("home.html")    
  
             

@app.route("/checkin", methods=["GET", "POST"])
def checkin():
    if "email" not in session:
        session['path'] = request.url
        return redirect(url_for("signin"))
    user = User.query.filter_by(email = session["email"]).first()
    #print(user)
    if user is None:
        session['path'] = request.url
        return redirect(url_for("signin"))
    elif user.email =="careerclosetatm@gmail.com":
        form = CheckinForm()
        if request.method == "POST":
            if form.validate() == False:
                flash("All fields are required")
                return render_template("checkin.html", form=form)
            else:
                suits = Suits.query.filter(Suits.suit_id == form.suiteId.data.upper()).first()                
                if suits != None:
                    suits.available = True
                    db.session.commit()  
                    checkinDate = datetime.now().date()
                    
                suits = Suits.query.filter(Suits.available==False).all()
                return render_template("checkin.html", success = True, form=form, suits=suits)
        elif request.method == "GET":
            suits = Suits.query.filter(Suits.available==False).all()                               
            return render_template("checkin.html", form=form, suits=suits)  
    else:
        return render_template("home.html")
    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Renders a template to take the user to the sign up Screen upon Get request. 
     Takes the user to the Home screen upon Post request after the sign up.
     Also, updates the database with the details of the signed up user.
    """ 
    form = SignupForm()   
    if request.method == 'POST':        
        if form.validate() == False:                   
            for field in form: 
                for error in field.errors:
                    print(error)     
                    
            return render_template('signup.html', form=form)
        else:            
            newuser = User(form.username.data,  form.fullname.data, form.email.data, form.uin.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()   
            session["email"] = newuser.email
            session["fullname"] = newuser.fullname            
            return redirect(url_for("home"))
   
    elif request.method == 'GET':
        print "get request"
        return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    """Renders a template to take the user to the sign-in Screen upon Get request. 
     Takes the user to the Home screen upon Post request if the there is no redirect url present in the session.
     Takes the user to the redirect url stored in the session upon post request, if the redirect url is not empty.
    """ 
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            user = User.query.filter_by(email = session["email"]).first()
            if user is None:
                return redirect(url_for("signin"))
            else:
                session['fullname'] = user.fullname  
            if "path" in session:           
                path = session['path']
            else:
                path = None
            session['path'] = None
            if path is not None: return redirect(path) 
            return redirect(url_for('home'))
                 
    elif request.method == 'GET':
        return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
    """Renders a template to take the user to the Home up Screen.
    """ 
 
    if 'email' not in session:
        #session['path'] = request.url
        return redirect(url_for('signin'))
     
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route("/availability", methods=["GET"])
def availability():
    """Renders a template to take the user to the Availability Screen. 
    Fetches the list of suit from the database based on the choice of the suit type.
    """ 

    form = AvailabilityForm()       
    suits = Suits.query.filter().all()
    #total count
    tmj = [0,0,0,0,0]
    tmp = [0,0,0,0,0]
    tfj = [0,0,0,0,0]
    tfp = [0,0,0,0,0]
    #actual count
    mj = [0,0,0,0,0]
    mp = [0,0,0,0,0]
    fj = [0,0,0,0,0]
    fp = [0,0,0,0,0]
    
    print(len(suits))
    for suit in suits:          
        if suit.gender.lower()=="m" and suit.type.lower()=="jacket" and suit.size.lower()=="s": tmj[0] = tmj[0]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="jacket" and suit.size.lower()=="m": tmj[1] = tmj[1]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="jacket" and suit.size.lower()=="l": tmj[2] = tmj[2]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="jacket" and suit.size.lower()=="xl": tmj[3] = tmj[3]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="jacket" and suit.size.lower()=="xxl": tmj[4] = tmj[4]+1
        
        if suit.gender.lower()=="m" and suit.type.lower()=="pant" and suit.size.lower()=="s": tmp[0] = tmp[0]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="pant" and suit.size.lower()=="m": tmp[1] = tmp[1]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="pant" and suit.size.lower()=="l": tmp[2] = tmp[2]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="pant" and suit.size.lower()=="xl": tmp[3] = tmp[3]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="pant" and suit.size.lower()=="xxl": tmp[4] = tmp[4]+1
        
        if suit.gender.lower()=="f" and suit.type.lower()=="jacket" and suit.size.lower()=="s": tfj[0] = tfj[0]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="jacket" and suit.size.lower()=="m": tfj[1] = tfj[1]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="jacket" and suit.size.lower()=="l": tfj[2] = tfj[2]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="jacket" and suit.size.lower()=="xl": tfj[3] = tfj[3]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="jacket" and suit.size.lower()=="xxl": tfj[4] = tfj[4]+1
        
        if suit.gender.lower()=="f" and suit.type.lower()=="pant" and suit.size.lower()=="s": tfp[0] = tfp[0]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="pant" and suit.size.lower()=="m": tfp[1] = tfp[1]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="pant" and suit.size.lower()=="l": tfp[2] = tfp[2]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="pant" and suit.size.lower()=="xl": tfp[3] = tfp[3]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="pant" and suit.size.lower()=="xxl": tfp[4] = tfp[4]+1
        
        # Actual
        if suit.gender.lower()=="m" and suit.type.lower()=="jacket" and suit.size.lower()=="s" and suit.available==True : mj[0] = mj[0]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="jacket" and suit.size.lower()=="m" and suit.available==True : mj[1] = mj[1]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="jacket" and suit.size.lower()=="l" and suit.available==True : mj[2] = mj[2]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="jacket" and suit.size.lower()=="xl" and suit.available==True : mj[3] = mj[3]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="jacket" and suit.size.lower()=="xxl" and suit.available==True : mj[4] = mj[4]+1
        
        if suit.gender.lower()=="m" and suit.type.lower()=="pant" and suit.size.lower()=="s" and suit.available==True : mp[0] = mp[0]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="pant" and suit.size.lower()=="m" and suit.available==True : mp[1] = mp[1]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="pant" and suit.size.lower()=="l" and suit.available==True : mp[2] = mp[2]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="pant" and suit.size.lower()=="xl" and suit.available==True : mp[3] = mp[3]+1
        if suit.gender.lower()=="m" and suit.type.lower()=="pant" and suit.size.lower()=="xxl" and suit.available==True : mp[4] = mp[4]+1
        
        if suit.gender.lower()=="f" and suit.type.lower()=="jacket" and suit.size.lower()=="s" and suit.available==True : fj[0] = fj[0]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="jacket" and suit.size.lower()=="m" and suit.available==True : fj[1] = fj[1]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="jacket" and suit.size.lower()=="l" and suit.available==True : fj[2] = fj[2]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="jacket" and suit.size.lower()=="xl" and suit.available==True : fj[3] = fj[3]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="jacket" and suit.size.lower()=="xxl" and suit.available==True : fj[4] = fj[4]+1
        
        if suit.gender.lower()=="f" and suit.type.lower()=="pant" and suit.size.lower()=="s" and suit.available==True : fp[0] = fp[0]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="pant" and suit.size.lower()=="m" and suit.available==True : fp[1] = fp[1]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="pant" and suit.size.lower()=="l" and suit.available==True : fp[2] = fp[2]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="pant" and suit.size.lower()=="xl" and suit.available==True : fp[3] = fp[3]+1
        if suit.gender.lower()=="f" and suit.type.lower()=="pant" and suit.size.lower()=="xxl" and suit.available==True : fp[4] = fp[4]+1
            
        #suits = Suits.query.filter(Suits.type == form.type.data).all()
    return render_template("availability.html", success = True, suits = suits, mj=mj, mp=mp, fj=fj, fp=fp,tmj=tmj, tmp=tmp, tfj=tfj, tfp=tfp,)
        

@app.route('/schedule/', methods=['GET'])
def schedule():
    print("Entered echo")
    dateValue = request.args.get('date')
    slots = Schedule.query.filter(Schedule.date_Value == datetime.strftime(datetime.strptime(dateValue,'%m/%d/%Y'),'%Y-%m-%d')).first()
    slotValue = Schedule.query.filter().all()
    return jsonify(result = {"date_Value":slots.date_Value, "time9_00":slots.time9_00, "time9_30":slots.time9_30, "time10_00":slots.time10_00, "time10_30":slots.time10_30, "time11_00":slots.time11_00, "time11_30":slots.time11_30, "time12_00":slots.time12_00, "time12_30":slots.time12_30, "time13_00":slots.time13_00, "time13_30":slots.time13_30, "time14_00":slots.time14_00, "time14_30":slots.time14_30, "time15_00":slots.time15_00, "time15_30":slots.time15_30, "time16_00":slots.time16_00, "time16_30":slots.time16_30,"time17_00":slots.time17_00})    
    
@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/appointment", methods=['GET', 'POST'])
def appointment():
    """Renders a template to take the user to the Appointment screen. 
     Upon Post request updates the time field in the database for the appointment scheduled. Also, sends out an email to the user
     as a confirmation of the appointment.  
    """ 
    if "email" not in session:
        session['path'] = request.url
        return redirect(url_for("signin"))
    user = User.query.filter_by(email = session["email"]).first()
    if user is None:
        session['path'] = request.url
        return redirect(url_for("signin"))
    
    else:
        if request.method == 'POST':
            form = AppointmentForm()
            time_val = request.form["optradio"]            
            d_val = request.form["date_val"]
            date_val = datetime.strptime(d_val, "%m/%d/%Y")
            date_val = datetime.strftime(date_val, "%Y-%m-%d")
            db.session.add(Appointment(user_id=user.user_id,date_Value=date_val,time=time_val))
            schedule_Value = Schedule.query.filter(Schedule.date_Value == date_val).first()
            setattr(schedule_Value, time_val, False)
            db.session.commit()        
            schedule_Value = Schedule.query.filter(Schedule.date_Value == date_val).first()
            print(schedule_Value.time12_00)
            
            msg = Message("Confirmation of your appointment with the Career Closet",
                              sender='careerclosetatm@gmail.com',
                              recipients=[session["email"]])
#             msg.body = """
#                 From: Team Career Closet <%s>,
#                 Howdy %s, 
#                 This is a confirmation of your appointment with the Career Closet on %s at %s. Please turn up with your Tamu student ID card on the above mentioned date and time.
#                 Gigem.
#                 Team Career Closet.
#                 """ % ('careerclosetatm@gmail.com',user.fullname,date_val,time_val)
            msg.body = """
Howdy %s, 
This is a confirmation of your appointment with the Career Closet on %s at %s. Please turn up with your Tamu student ID card on the above mentioned date and time.
Gigem.
Team Career Closet.
""" % (user.fullname,date_val,time_val)
            
            mail.send(msg)
            return render_template("appointment.html", success=True)
        return render_template("appointment.html")
            
    
@app.route("/404")
def error():
    """Renders a template to take the user to the 404 Screen upon hitting an error page. 
    """ 
    return render_template("404.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Renders a template to take the user to the Contact Screen. 
     Takes the user to the Contact screen upon Get request.
     Also, sends an email to careerclosetatm@gmail.com if the users has any information to share with the Career Closet.
    """ 

    form = ContactForm()
    
    if request.method == "POST":
         msg = Message("Message from your visitor" + form.name.data,
                          sender=form.email.data,
                          recipients=['careerclosetatm@gmail.com'])
         msg.body = """
            From: %s <%s>,
            %s
            """ % (form.name.data, form.email.data, form.message.data)
         mail.send(msg)
         return render_template("contact.html", success = True)
    elif request.method == "GET":
        return render_template("contact.html", form=form)
        
        
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
app.secret_key = "12345667"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'careerclosetatm@gmail.com'
app.config["MAIL_PASSWORD"] = 'Group5Password'
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development'
from models import db
db.init_app(app)    
with app.test_request_context():
    #db.drop_all()
    #Creating schedule DB
    db.create_all()
    '''
    Data inserted in the database for appointment and suit information.
    
    schedule1=Schedule("2017-04-06",False,True,True,True,False,True,True,True,True,True,True,True,False,True,True,True,True)
    schedule2=Schedule("2017-04-07",True,True,False,True,True,True,False,False,True,True,True,True,True,True,True,True,True)
    schedule3=Schedule("2017-04-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule4=Schedule("2017-04-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule5=Schedule("2017-04-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule6=Schedule("2017-04-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule7=Schedule("2017-04-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule8=Schedule("2017-04-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule9=Schedule("2017-04-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule10=Schedule("2017-04-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule11=Schedule("2017-04-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule12=Schedule("2017-04-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule13=Schedule("2017-04-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule14=Schedule("2017-04-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule15=Schedule("2017-04-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule16=Schedule("2017-04-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule17=Schedule("2017-04-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule18=Schedule("2017-05-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule19=Schedule("2017-05-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule20=Schedule("2017-05-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule21=Schedule("2017-05-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule22=Schedule("2017-05-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule23=Schedule("2017-05-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule24=Schedule("2017-05-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule25=Schedule("2017-05-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule26=Schedule("2017-05-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule27=Schedule("2017-05-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule28=Schedule("2017-05-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule29=Schedule("2017-05-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule30=Schedule("2017-05-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule31=Schedule("2017-05-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule32=Schedule("2017-05-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule33=Schedule("2017-05-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule34=Schedule("2017-05-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule35=Schedule("2017-05-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule36=Schedule("2017-05-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule37=Schedule("2017-05-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule38=Schedule("2017-05-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule39=Schedule("2017-05-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule40=Schedule("2017-05-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule41=Schedule("2017-06-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule42=Schedule("2017-06-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule43=Schedule("2017-06-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule44=Schedule("2017-06-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule45=Schedule("2017-06-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule46=Schedule("2017-06-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule47=Schedule("2017-06-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule48=Schedule("2017-06-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule49=Schedule("2017-06-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule50=Schedule("2017-06-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule51=Schedule("2017-06-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule52=Schedule("2017-06-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule53=Schedule("2017-06-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule54=Schedule("2017-06-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule55=Schedule("2017-06-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule56=Schedule("2017-06-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule57=Schedule("2017-06-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule58=Schedule("2017-06-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule59=Schedule("2017-06-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule60=Schedule("2017-06-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule61=Schedule("2017-06-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule62=Schedule("2017-06-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule63=Schedule("2017-07-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule64=Schedule("2017-07-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule65=Schedule("2017-07-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule66=Schedule("2017-07-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule67=Schedule("2017-07-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule68=Schedule("2017-07-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule69=Schedule("2017-07-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule70=Schedule("2017-07-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule71=Schedule("2017-07-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule72=Schedule("2017-07-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule73=Schedule("2017-07-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule74=Schedule("2017-07-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule75=Schedule("2017-07-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule76=Schedule("2017-07-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule77=Schedule("2017-07-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule78=Schedule("2017-07-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule79=Schedule("2017-07-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule80=Schedule("2017-07-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule81=Schedule("2017-07-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule82=Schedule("2017-07-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule83=Schedule("2017-07-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule84=Schedule("2017-08-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule85=Schedule("2017-08-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule86=Schedule("2017-08-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule87=Schedule("2017-08-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule88=Schedule("2017-08-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule89=Schedule("2017-08-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule90=Schedule("2017-08-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule91=Schedule("2017-08-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule92=Schedule("2017-08-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule93=Schedule("2017-08-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule94=Schedule("2017-08-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule95=Schedule("2017-08-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule96=Schedule("2017-08-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule97=Schedule("2017-08-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule98=Schedule("2017-08-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule99=Schedule("2017-08-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule100=Schedule("2017-08-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule101=Schedule("2017-08-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule102=Schedule("2017-08-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule103=Schedule("2017-08-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule104=Schedule("2017-08-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule105=Schedule("2017-08-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule106=Schedule("2017-08-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule107=Schedule("2017-09-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule108=Schedule("2017-09-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule109=Schedule("2017-09-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule110=Schedule("2017-09-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule111=Schedule("2017-09-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule112=Schedule("2017-09-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule113=Schedule("2017-09-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule114=Schedule("2017-09-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule115=Schedule("2017-09-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule116=Schedule("2017-09-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule117=Schedule("2017-09-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule118=Schedule("2017-09-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule119=Schedule("2017-09-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule120=Schedule("2017-09-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule121=Schedule("2017-09-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule122=Schedule("2017-09-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule123=Schedule("2017-09-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule124=Schedule("2017-09-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule125=Schedule("2017-09-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule126=Schedule("2017-09-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule127=Schedule("2017-09-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule128=Schedule("2017-10-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule129=Schedule("2017-10-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule130=Schedule("2017-10-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule131=Schedule("2017-10-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule132=Schedule("2017-10-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule133=Schedule("2017-10-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule134=Schedule("2017-10-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule135=Schedule("2017-10-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule136=Schedule("2017-10-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule137=Schedule("2017-10-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule138=Schedule("2017-10-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule139=Schedule("2017-10-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule140=Schedule("2017-10-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule141=Schedule("2017-10-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule142=Schedule("2017-10-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule143=Schedule("2017-10-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule144=Schedule("2017-10-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule145=Schedule("2017-10-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule146=Schedule("2017-10-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule147=Schedule("2017-10-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule148=Schedule("2017-10-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule149=Schedule("2017-10-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule150=Schedule("2017-11-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule151=Schedule("2017-11-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule152=Schedule("2017-11-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule153=Schedule("2017-11-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule154=Schedule("2017-11-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule155=Schedule("2017-11-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule156=Schedule("2017-11-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule157=Schedule("2017-11-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule158=Schedule("2017-11-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule159=Schedule("2017-11-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule160=Schedule("2017-11-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule161=Schedule("2017-11-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule162=Schedule("2017-11-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule163=Schedule("2017-11-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule164=Schedule("2017-11-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule165=Schedule("2017-11-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule166=Schedule("2017-11-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule167=Schedule("2017-11-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule168=Schedule("2017-11-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule169=Schedule("2017-11-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule170=Schedule("2017-11-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule171=Schedule("2017-11-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule172=Schedule("2017-12-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule173=Schedule("2017-12-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule174=Schedule("2017-12-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule175=Schedule("2017-12-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule176=Schedule("2017-12-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule177=Schedule("2017-12-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule178=Schedule("2017-12-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule179=Schedule("2017-12-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule180=Schedule("2017-12-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule181=Schedule("2017-12-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule182=Schedule("2017-12-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule183=Schedule("2017-12-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule184=Schedule("2017-12-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule185=Schedule("2017-12-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule186=Schedule("2017-12-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule187=Schedule("2017-12-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule188=Schedule("2017-12-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule189=Schedule("2017-12-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule190=Schedule("2017-12-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule191=Schedule("2017-12-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule192=Schedule("2017-12-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule193=Schedule("2018-01-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule194=Schedule("2018-01-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule195=Schedule("2018-01-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule196=Schedule("2018-01-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule197=Schedule("2018-01-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule198=Schedule("2018-01-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule199=Schedule("2018-01-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule200=Schedule("2018-01-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule201=Schedule("2018-01-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule202=Schedule("2018-01-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule203=Schedule("2018-01-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule204=Schedule("2018-01-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule205=Schedule("2018-01-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule206=Schedule("2018-01-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule207=Schedule("2018-01-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule208=Schedule("2018-01-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule209=Schedule("2018-01-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule210=Schedule("2018-01-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule211=Schedule("2018-01-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule212=Schedule("2018-01-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule213=Schedule("2018-01-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule214=Schedule("2018-01-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule215=Schedule("2018-01-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule216=Schedule("2018-02-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule217=Schedule("2018-02-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule218=Schedule("2018-02-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule219=Schedule("2018-02-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule220=Schedule("2018-02-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule221=Schedule("2018-02-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule222=Schedule("2018-02-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule223=Schedule("2018-02-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule224=Schedule("2018-02-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule225=Schedule("2018-02-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule226=Schedule("2018-02-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule227=Schedule("2018-02-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule228=Schedule("2018-02-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule229=Schedule("2018-02-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule230=Schedule("2018-02-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule231=Schedule("2018-02-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule232=Schedule("2018-02-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule233=Schedule("2018-02-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule234=Schedule("2018-02-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule235=Schedule("2018-02-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule236=Schedule("2018-03-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule237=Schedule("2018-03-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule238=Schedule("2018-03-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule239=Schedule("2018-03-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule240=Schedule("2018-03-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule241=Schedule("2018-03-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule242=Schedule("2018-03-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule243=Schedule("2018-03-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule244=Schedule("2018-03-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule245=Schedule("2018-03-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule246=Schedule("2018-03-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule247=Schedule("2018-03-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule248=Schedule("2018-03-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule249=Schedule("2018-03-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule250=Schedule("2018-03-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule251=Schedule("2018-03-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule252=Schedule("2018-03-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule253=Schedule("2018-03-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule254=Schedule("2018-03-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule255=Schedule("2018-03-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule256=Schedule("2018-03-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule257=Schedule("2018-03-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule258=Schedule("2018-04-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule259=Schedule("2018-04-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule260=Schedule("2018-04-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule261=Schedule("2018-04-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule262=Schedule("2018-04-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule263=Schedule("2018-04-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule264=Schedule("2018-04-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule265=Schedule("2018-04-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule266=Schedule("2018-04-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule267=Schedule("2018-04-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule268=Schedule("2018-04-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule269=Schedule("2018-04-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule270=Schedule("2018-04-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule271=Schedule("2018-04-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule272=Schedule("2018-04-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule273=Schedule("2018-04-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule274=Schedule("2018-04-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule275=Schedule("2018-04-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule276=Schedule("2018-04-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule277=Schedule("2018-04-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule278=Schedule("2018-04-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule279=Schedule("2018-05-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule280=Schedule("2018-05-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule281=Schedule("2018-05-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule282=Schedule("2018-05-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule283=Schedule("2018-05-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule284=Schedule("2018-05-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule285=Schedule("2018-05-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule286=Schedule("2018-05-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule287=Schedule("2018-05-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule288=Schedule("2018-05-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule289=Schedule("2018-05-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule290=Schedule("2018-05-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule291=Schedule("2018-05-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule292=Schedule("2018-05-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule293=Schedule("2018-05-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule294=Schedule("2018-05-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule295=Schedule("2018-05-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule296=Schedule("2018-05-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule297=Schedule("2018-05-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule298=Schedule("2018-05-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule299=Schedule("2018-05-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule300=Schedule("2018-05-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule301=Schedule("2018-05-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule302=Schedule("2018-06-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule303=Schedule("2018-06-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule304=Schedule("2018-06-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule305=Schedule("2018-06-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule306=Schedule("2018-06-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule307=Schedule("2018-06-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule308=Schedule("2018-06-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule309=Schedule("2018-06-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule310=Schedule("2018-06-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule311=Schedule("2018-06-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule312=Schedule("2018-06-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule313=Schedule("2018-06-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule314=Schedule("2018-06-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule315=Schedule("2018-06-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule316=Schedule("2018-06-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule317=Schedule("2018-06-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule318=Schedule("2018-06-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule319=Schedule("2018-06-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule320=Schedule("2018-06-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule321=Schedule("2018-06-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule322=Schedule("2018-06-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule323=Schedule("2018-07-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule324=Schedule("2018-07-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule325=Schedule("2018-07-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule326=Schedule("2018-07-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule327=Schedule("2018-07-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule328=Schedule("2018-07-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule329=Schedule("2018-07-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule330=Schedule("2018-07-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule331=Schedule("2018-07-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule332=Schedule("2018-07-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule333=Schedule("2018-07-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule334=Schedule("2018-07-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule335=Schedule("2018-07-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule336=Schedule("2018-07-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule337=Schedule("2018-07-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule338=Schedule("2018-07-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule339=Schedule("2018-07-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule340=Schedule("2018-07-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule341=Schedule("2018-07-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule342=Schedule("2018-07-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule343=Schedule("2018-07-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule344=Schedule("2018-07-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule345=Schedule("2018-08-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule346=Schedule("2018-08-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule347=Schedule("2018-08-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule348=Schedule("2018-08-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule349=Schedule("2018-08-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule350=Schedule("2018-08-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule351=Schedule("2018-08-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule352=Schedule("2018-08-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule353=Schedule("2018-08-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule354=Schedule("2018-08-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule355=Schedule("2018-08-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule356=Schedule("2018-08-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule357=Schedule("2018-08-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule358=Schedule("2018-08-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule359=Schedule("2018-08-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule360=Schedule("2018-08-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule361=Schedule("2018-08-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule362=Schedule("2018-08-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule363=Schedule("2018-08-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule364=Schedule("2018-08-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule365=Schedule("2018-08-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule366=Schedule("2018-08-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule367=Schedule("2018-08-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule368=Schedule("2018-09-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule369=Schedule("2018-09-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule370=Schedule("2018-09-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule371=Schedule("2018-09-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule372=Schedule("2018-09-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule373=Schedule("2018-09-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule374=Schedule("2018-09-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule375=Schedule("2018-09-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule376=Schedule("2018-09-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule377=Schedule("2018-09-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule378=Schedule("2018-09-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule379=Schedule("2018-09-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule380=Schedule("2018-09-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule381=Schedule("2018-09-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule382=Schedule("2018-09-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule383=Schedule("2018-09-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule384=Schedule("2018-09-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule385=Schedule("2018-09-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule386=Schedule("2018-09-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule387=Schedule("2018-09-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule388=Schedule("2018-10-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule389=Schedule("2018-10-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule390=Schedule("2018-10-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule391=Schedule("2018-10-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule392=Schedule("2018-10-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule393=Schedule("2018-10-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule394=Schedule("2018-10-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule395=Schedule("2018-10-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule396=Schedule("2018-10-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule397=Schedule("2018-10-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule398=Schedule("2018-10-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule399=Schedule("2018-10-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule400=Schedule("2018-10-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule401=Schedule("2018-10-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule402=Schedule("2018-10-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule403=Schedule("2018-10-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule404=Schedule("2018-10-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule405=Schedule("2018-10-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule406=Schedule("2018-10-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule407=Schedule("2018-10-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule408=Schedule("2018-10-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule409=Schedule("2018-10-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule410=Schedule("2018-10-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule411=Schedule("2018-11-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule412=Schedule("2018-11-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule413=Schedule("2018-11-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule414=Schedule("2018-11-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule415=Schedule("2018-11-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule416=Schedule("2018-11-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule417=Schedule("2018-11-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule418=Schedule("2018-11-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule419=Schedule("2018-11-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule420=Schedule("2018-11-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule421=Schedule("2018-11-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule422=Schedule("2018-11-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule423=Schedule("2018-11-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule424=Schedule("2018-11-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule425=Schedule("2018-11-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule426=Schedule("2018-11-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule427=Schedule("2018-11-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule428=Schedule("2018-11-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule429=Schedule("2018-11-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule430=Schedule("2018-11-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule431=Schedule("2018-11-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule432=Schedule("2018-11-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule433=Schedule("2018-12-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule434=Schedule("2018-12-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule435=Schedule("2018-12-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule436=Schedule("2018-12-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule437=Schedule("2018-12-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule438=Schedule("2018-12-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule439=Schedule("2018-12-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule440=Schedule("2018-12-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule441=Schedule("2018-12-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule442=Schedule("2018-12-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule443=Schedule("2018-12-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule444=Schedule("2018-12-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule445=Schedule("2018-12-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule446=Schedule("2018-12-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule447=Schedule("2018-12-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule448=Schedule("2018-12-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule449=Schedule("2018-12-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule450=Schedule("2018-12-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule451=Schedule("2018-12-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule452=Schedule("2018-12-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule453=Schedule("2018-12-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule454=Schedule("2019-01-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule455=Schedule("2019-01-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule456=Schedule("2019-01-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule457=Schedule("2019-01-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule458=Schedule("2019-01-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule459=Schedule("2019-01-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule460=Schedule("2019-01-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule461=Schedule("2019-01-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule462=Schedule("2019-01-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule463=Schedule("2019-01-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule464=Schedule("2019-01-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule465=Schedule("2019-01-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule466=Schedule("2019-01-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule467=Schedule("2019-01-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule468=Schedule("2019-01-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule469=Schedule("2019-01-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule470=Schedule("2019-01-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule471=Schedule("2019-01-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule472=Schedule("2019-01-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule473=Schedule("2019-01-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule474=Schedule("2019-01-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule475=Schedule("2019-01-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule476=Schedule("2019-01-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule477=Schedule("2019-02-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule478=Schedule("2019-02-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule479=Schedule("2019-02-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule480=Schedule("2019-02-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule481=Schedule("2019-02-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule482=Schedule("2019-02-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule483=Schedule("2019-02-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule484=Schedule("2019-02-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule485=Schedule("2019-02-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule486=Schedule("2019-02-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule487=Schedule("2019-02-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule488=Schedule("2019-02-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule489=Schedule("2019-02-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule490=Schedule("2019-02-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule491=Schedule("2019-02-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule492=Schedule("2019-02-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule493=Schedule("2019-02-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule494=Schedule("2019-02-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule495=Schedule("2019-02-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule496=Schedule("2019-02-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule497=Schedule("2019-03-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule498=Schedule("2019-03-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule499=Schedule("2019-03-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule500=Schedule("2019-03-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule501=Schedule("2019-03-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule502=Schedule("2019-03-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule503=Schedule("2019-03-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule504=Schedule("2019-03-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule505=Schedule("2019-03-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule506=Schedule("2019-03-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule507=Schedule("2019-03-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule508=Schedule("2019-03-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule509=Schedule("2019-03-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule510=Schedule("2019-03-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule511=Schedule("2019-03-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule512=Schedule("2019-03-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule513=Schedule("2019-03-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule514=Schedule("2019-03-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule515=Schedule("2019-03-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule516=Schedule("2019-03-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule517=Schedule("2019-03-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule518=Schedule("2019-04-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule519=Schedule("2019-04-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule520=Schedule("2019-04-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule521=Schedule("2019-04-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule522=Schedule("2019-04-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule523=Schedule("2019-04-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule524=Schedule("2019-04-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule525=Schedule("2019-04-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule526=Schedule("2019-04-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule527=Schedule("2019-04-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule528=Schedule("2019-04-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule529=Schedule("2019-04-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule530=Schedule("2019-04-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule531=Schedule("2019-04-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule532=Schedule("2019-04-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule533=Schedule("2019-04-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule534=Schedule("2019-04-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule535=Schedule("2019-04-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule536=Schedule("2019-04-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule537=Schedule("2019-04-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule538=Schedule("2019-04-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule539=Schedule("2019-04-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule540=Schedule("2019-05-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule541=Schedule("2019-05-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule542=Schedule("2019-05-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule543=Schedule("2019-05-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule544=Schedule("2019-05-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule545=Schedule("2019-05-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule546=Schedule("2019-05-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule547=Schedule("2019-05-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule548=Schedule("2019-05-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule549=Schedule("2019-05-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule550=Schedule("2019-05-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule551=Schedule("2019-05-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule552=Schedule("2019-05-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule553=Schedule("2019-05-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule554=Schedule("2019-05-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule555=Schedule("2019-05-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule556=Schedule("2019-05-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule557=Schedule("2019-05-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule558=Schedule("2019-05-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule559=Schedule("2019-05-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule560=Schedule("2019-05-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule561=Schedule("2019-05-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule562=Schedule("2019-05-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule563=Schedule("2019-06-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule564=Schedule("2019-06-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule565=Schedule("2019-06-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule566=Schedule("2019-06-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule567=Schedule("2019-06-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule568=Schedule("2019-06-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule569=Schedule("2019-06-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule570=Schedule("2019-06-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule571=Schedule("2019-06-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule572=Schedule("2019-06-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule573=Schedule("2019-06-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule574=Schedule("2019-06-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule575=Schedule("2019-06-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule576=Schedule("2019-06-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule577=Schedule("2019-06-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule578=Schedule("2019-06-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule579=Schedule("2019-06-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule580=Schedule("2019-06-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule581=Schedule("2019-06-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule582=Schedule("2019-06-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule583=Schedule("2019-07-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule584=Schedule("2019-07-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule585=Schedule("2019-07-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule586=Schedule("2019-07-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule587=Schedule("2019-07-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule588=Schedule("2019-07-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule589=Schedule("2019-07-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule590=Schedule("2019-07-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule591=Schedule("2019-07-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule592=Schedule("2019-07-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule593=Schedule("2019-07-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule594=Schedule("2019-07-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule595=Schedule("2019-07-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule596=Schedule("2019-07-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule597=Schedule("2019-07-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule598=Schedule("2019-07-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule599=Schedule("2019-07-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule600=Schedule("2019-07-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule601=Schedule("2019-07-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule602=Schedule("2019-07-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule603=Schedule("2019-07-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule604=Schedule("2019-07-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule605=Schedule("2019-07-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule606=Schedule("2019-08-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule607=Schedule("2019-08-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule608=Schedule("2019-08-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule609=Schedule("2019-08-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule610=Schedule("2019-08-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule611=Schedule("2019-08-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule612=Schedule("2019-08-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule613=Schedule("2019-08-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule614=Schedule("2019-08-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule615=Schedule("2019-08-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule616=Schedule("2019-08-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule617=Schedule("2019-08-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule618=Schedule("2019-08-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule619=Schedule("2019-08-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule620=Schedule("2019-08-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule621=Schedule("2019-08-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule622=Schedule("2019-08-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule623=Schedule("2019-08-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule624=Schedule("2019-08-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule625=Schedule("2019-08-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule626=Schedule("2019-08-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule627=Schedule("2019-08-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule628=Schedule("2019-09-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule629=Schedule("2019-09-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule630=Schedule("2019-09-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule631=Schedule("2019-09-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule632=Schedule("2019-09-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule633=Schedule("2019-09-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule634=Schedule("2019-09-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule635=Schedule("2019-09-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule636=Schedule("2019-09-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule637=Schedule("2019-09-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule638=Schedule("2019-09-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule639=Schedule("2019-09-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule640=Schedule("2019-09-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule641=Schedule("2019-09-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule642=Schedule("2019-09-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule643=Schedule("2019-09-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule644=Schedule("2019-09-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule645=Schedule("2019-09-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule646=Schedule("2019-09-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule647=Schedule("2019-09-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule648=Schedule("2019-09-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule649=Schedule("2019-10-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule650=Schedule("2019-10-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule651=Schedule("2019-10-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule652=Schedule("2019-10-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule653=Schedule("2019-10-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule654=Schedule("2019-10-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule655=Schedule("2019-10-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule656=Schedule("2019-10-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule657=Schedule("2019-10-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule658=Schedule("2019-10-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule659=Schedule("2019-10-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule660=Schedule("2019-10-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule661=Schedule("2019-10-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule662=Schedule("2019-10-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule663=Schedule("2019-10-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule664=Schedule("2019-10-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule665=Schedule("2019-10-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule666=Schedule("2019-10-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule667=Schedule("2019-10-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule668=Schedule("2019-10-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule669=Schedule("2019-10-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule670=Schedule("2019-10-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule671=Schedule("2019-10-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule672=Schedule("2019-11-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule673=Schedule("2019-11-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule674=Schedule("2019-11-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule675=Schedule("2019-11-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule676=Schedule("2019-11-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule677=Schedule("2019-11-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule678=Schedule("2019-11-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule679=Schedule("2019-11-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule680=Schedule("2019-11-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule681=Schedule("2019-11-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule682=Schedule("2019-11-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule683=Schedule("2019-11-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule684=Schedule("2019-11-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule685=Schedule("2019-11-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule686=Schedule("2019-11-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule687=Schedule("2019-11-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule688=Schedule("2019-11-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule689=Schedule("2019-11-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule690=Schedule("2019-11-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule691=Schedule("2019-11-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule692=Schedule("2019-11-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule693=Schedule("2019-12-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule694=Schedule("2019-12-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule695=Schedule("2019-12-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule696=Schedule("2019-12-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule697=Schedule("2019-12-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule698=Schedule("2019-12-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule699=Schedule("2019-12-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule700=Schedule("2019-12-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule701=Schedule("2019-12-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule702=Schedule("2019-12-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule703=Schedule("2019-12-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule704=Schedule("2019-12-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule705=Schedule("2019-12-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule706=Schedule("2019-12-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule707=Schedule("2019-12-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule708=Schedule("2019-12-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule709=Schedule("2019-12-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule710=Schedule("2019-12-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule711=Schedule("2019-12-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule712=Schedule("2019-12-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule713=Schedule("2019-12-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule714=Schedule("2019-12-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule715=Schedule("2020-01-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule716=Schedule("2020-01-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule717=Schedule("2020-01-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule718=Schedule("2020-01-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule719=Schedule("2020-01-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule720=Schedule("2020-01-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule721=Schedule("2020-01-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule722=Schedule("2020-01-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule723=Schedule("2020-01-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule724=Schedule("2020-01-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule725=Schedule("2020-01-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule726=Schedule("2020-01-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule727=Schedule("2020-01-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule728=Schedule("2020-01-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule729=Schedule("2020-01-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule730=Schedule("2020-01-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule731=Schedule("2020-01-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule732=Schedule("2020-01-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule733=Schedule("2020-01-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule734=Schedule("2020-01-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule735=Schedule("2020-01-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule736=Schedule("2020-01-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule737=Schedule("2020-01-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule738=Schedule("2020-02-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule739=Schedule("2020-02-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule740=Schedule("2020-02-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule741=Schedule("2020-02-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule742=Schedule("2020-02-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule743=Schedule("2020-02-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule744=Schedule("2020-02-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule745=Schedule("2020-02-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule746=Schedule("2020-02-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule747=Schedule("2020-02-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule748=Schedule("2020-02-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule749=Schedule("2020-02-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule750=Schedule("2020-02-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule751=Schedule("2020-02-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule752=Schedule("2020-02-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule753=Schedule("2020-02-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule754=Schedule("2020-02-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule755=Schedule("2020-02-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule756=Schedule("2020-02-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule757=Schedule("2020-02-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule758=Schedule("2020-03-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule759=Schedule("2020-03-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule760=Schedule("2020-03-04",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule761=Schedule("2020-03-05",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule762=Schedule("2020-03-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule763=Schedule("2020-03-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule764=Schedule("2020-03-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule765=Schedule("2020-03-11",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule766=Schedule("2020-03-12",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule767=Schedule("2020-03-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule768=Schedule("2020-03-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule769=Schedule("2020-03-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule770=Schedule("2020-03-18",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule771=Schedule("2020-03-19",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule772=Schedule("2020-03-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule773=Schedule("2020-03-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule774=Schedule("2020-03-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule775=Schedule("2020-03-25",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule776=Schedule("2020-03-26",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule777=Schedule("2020-03-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule778=Schedule("2020-03-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule779=Schedule("2020-03-31",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule780=Schedule("2020-04-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule781=Schedule("2020-04-02",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule782=Schedule("2020-04-03",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule783=Schedule("2020-04-06",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule784=Schedule("2020-04-07",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule785=Schedule("2020-04-08",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule786=Schedule("2020-04-09",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule787=Schedule("2020-04-10",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule788=Schedule("2020-04-13",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule789=Schedule("2020-04-14",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule790=Schedule("2020-04-15",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule791=Schedule("2020-04-16",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule792=Schedule("2020-04-17",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule793=Schedule("2020-04-20",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule794=Schedule("2020-04-21",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule795=Schedule("2020-04-22",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule796=Schedule("2020-04-23",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule797=Schedule("2020-04-24",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule798=Schedule("2020-04-27",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule799=Schedule("2020-04-28",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule800=Schedule("2020-04-29",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule801=Schedule("2020-04-30",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    schedule802=Schedule("2020-05-01",True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)        
    db.session.add(schedule1)
    db.session.add(schedule2)
    db.session.add(schedule3)
    db.session.add(schedule4)
    db.session.add(schedule5)
    db.session.add(schedule6)
    db.session.add(schedule7)
    db.session.add(schedule8)
    db.session.add(schedule9)
    db.session.add(schedule10)
    db.session.add(schedule11)
    db.session.add(schedule12)
    db.session.add(schedule13)
    db.session.add(schedule14)
    db.session.add(schedule15)
    db.session.add(schedule16)
    db.session.add(schedule17)
    db.session.add(schedule18)
    db.session.add(schedule19)
    db.session.add(schedule20)
    db.session.add(schedule21)
    db.session.add(schedule22)
    db.session.add(schedule23)
    db.session.add(schedule24)
    db.session.add(schedule25)
    db.session.add(schedule26)
    db.session.add(schedule27)
    db.session.add(schedule28)
    db.session.add(schedule29)
    db.session.add(schedule30)
    db.session.add(schedule31)
    db.session.add(schedule32)
    db.session.add(schedule33)
    db.session.add(schedule34)
    db.session.add(schedule35)
    db.session.add(schedule36)
    db.session.add(schedule37)
    db.session.add(schedule38)
    db.session.add(schedule39)
    db.session.add(schedule40)
    db.session.add(schedule41)
    db.session.add(schedule42)
    db.session.add(schedule43)
    db.session.add(schedule44)
    db.session.add(schedule45)
    db.session.add(schedule46)
    db.session.add(schedule47)
    db.session.add(schedule48)
    db.session.add(schedule49)
    db.session.add(schedule50)
    db.session.add(schedule51)
    db.session.add(schedule52)
    db.session.add(schedule53)
    db.session.add(schedule54)
    db.session.add(schedule55)
    db.session.add(schedule56)
    db.session.add(schedule57)
    db.session.add(schedule58)
    db.session.add(schedule59)
    db.session.add(schedule60)
    db.session.add(schedule61)
    db.session.add(schedule62)
    db.session.add(schedule63)
    db.session.add(schedule64)
    db.session.add(schedule65)
    db.session.add(schedule66)
    db.session.add(schedule67)
    db.session.add(schedule68)
    db.session.add(schedule69)
    db.session.add(schedule70)
    db.session.add(schedule71)
    db.session.add(schedule72)
    db.session.add(schedule73)
    db.session.add(schedule74)
    db.session.add(schedule75)
    db.session.add(schedule76)
    db.session.add(schedule77)
    db.session.add(schedule78)
    db.session.add(schedule79)
    db.session.add(schedule80)
    db.session.add(schedule81)
    db.session.add(schedule82)
    db.session.add(schedule83)
    db.session.add(schedule84)
    db.session.add(schedule85)
    db.session.add(schedule86)
    db.session.add(schedule87)
    db.session.add(schedule88)
    db.session.add(schedule89)
    db.session.add(schedule90)
    db.session.add(schedule91)
    db.session.add(schedule92)
    db.session.add(schedule93)
    db.session.add(schedule94)
    db.session.add(schedule95)
    db.session.add(schedule96)
    db.session.add(schedule97)
    db.session.add(schedule98)
    db.session.add(schedule99)
    db.session.add(schedule100)
    db.session.add(schedule101)
    db.session.add(schedule102)
    db.session.add(schedule103)
    db.session.add(schedule104)
    db.session.add(schedule105)
    db.session.add(schedule106)
    db.session.add(schedule107)
    db.session.add(schedule108)
    db.session.add(schedule109)
    db.session.add(schedule110)
    db.session.add(schedule111)
    db.session.add(schedule112)
    db.session.add(schedule113)
    db.session.add(schedule114)
    db.session.add(schedule115)
    db.session.add(schedule116)
    db.session.add(schedule117)
    db.session.add(schedule118)
    db.session.add(schedule119)
    db.session.add(schedule120)
    db.session.add(schedule121)
    db.session.add(schedule122)
    db.session.add(schedule123)
    db.session.add(schedule124)
    db.session.add(schedule125)
    db.session.add(schedule126)
    db.session.add(schedule127)
    db.session.add(schedule128)
    db.session.add(schedule129)
    db.session.add(schedule130)
    db.session.add(schedule131)
    db.session.add(schedule132)
    db.session.add(schedule133)
    db.session.add(schedule134)
    db.session.add(schedule135)
    db.session.add(schedule136)
    db.session.add(schedule137)
    db.session.add(schedule138)
    db.session.add(schedule139)
    db.session.add(schedule140)
    db.session.add(schedule141)
    db.session.add(schedule142)
    db.session.add(schedule143)
    db.session.add(schedule144)
    db.session.add(schedule145)
    db.session.add(schedule146)
    db.session.add(schedule147)
    db.session.add(schedule148)
    db.session.add(schedule149)
    db.session.add(schedule150)
    db.session.add(schedule151)
    db.session.add(schedule152)
    db.session.add(schedule153)
    db.session.add(schedule154)
    db.session.add(schedule155)
    db.session.add(schedule156)
    db.session.add(schedule157)
    db.session.add(schedule158)
    db.session.add(schedule159)
    db.session.add(schedule160)
    db.session.add(schedule161)
    db.session.add(schedule162)
    db.session.add(schedule163)
    db.session.add(schedule164)
    db.session.add(schedule165)
    db.session.add(schedule166)
    db.session.add(schedule167)
    db.session.add(schedule168)
    db.session.add(schedule169)
    db.session.add(schedule170)
    db.session.add(schedule171)
    db.session.add(schedule172)
    db.session.add(schedule173)
    db.session.add(schedule174)
    db.session.add(schedule175)
    db.session.add(schedule176)
    db.session.add(schedule177)
    db.session.add(schedule178)
    db.session.add(schedule179)
    db.session.add(schedule180)
    db.session.add(schedule181)
    db.session.add(schedule182)
    db.session.add(schedule183)
    db.session.add(schedule184)
    db.session.add(schedule185)
    db.session.add(schedule186)
    db.session.add(schedule187)
    db.session.add(schedule188)
    db.session.add(schedule189)
    db.session.add(schedule190)
    db.session.add(schedule191)
    db.session.add(schedule192)
    db.session.add(schedule193)
    db.session.add(schedule194)
    db.session.add(schedule195)
    db.session.add(schedule196)
    db.session.add(schedule197)
    db.session.add(schedule198)
    db.session.add(schedule199)
    db.session.add(schedule200)
    db.session.add(schedule201)
    db.session.add(schedule202)
    db.session.add(schedule203)
    db.session.add(schedule204)
    db.session.add(schedule205)
    db.session.add(schedule206)
    db.session.add(schedule207)
    db.session.add(schedule208)
    db.session.add(schedule209)
    db.session.add(schedule210)
    db.session.add(schedule211)
    db.session.add(schedule212)
    db.session.add(schedule213)
    db.session.add(schedule214)
    db.session.add(schedule215)
    db.session.add(schedule216)
    db.session.add(schedule217)
    db.session.add(schedule218)
    db.session.add(schedule219)
    db.session.add(schedule220)
    db.session.add(schedule221)
    db.session.add(schedule222)
    db.session.add(schedule223)
    db.session.add(schedule224)
    db.session.add(schedule225)
    db.session.add(schedule226)
    db.session.add(schedule227)
    db.session.add(schedule228)
    db.session.add(schedule229)
    db.session.add(schedule230)
    db.session.add(schedule231)
    db.session.add(schedule232)
    db.session.add(schedule233)
    db.session.add(schedule234)
    db.session.add(schedule235)
    db.session.add(schedule236)
    db.session.add(schedule237)
    db.session.add(schedule238)
    db.session.add(schedule239)
    db.session.add(schedule240)
    db.session.add(schedule241)
    db.session.add(schedule242)
    db.session.add(schedule243)
    db.session.add(schedule244)
    db.session.add(schedule245)
    db.session.add(schedule246)
    db.session.add(schedule247)
    db.session.add(schedule248)
    db.session.add(schedule249)
    db.session.add(schedule250)
    db.session.add(schedule251)
    db.session.add(schedule252)
    db.session.add(schedule253)
    db.session.add(schedule254)
    db.session.add(schedule255)
    db.session.add(schedule256)
    db.session.add(schedule257)
    db.session.add(schedule258)
    db.session.add(schedule259)
    db.session.add(schedule260)
    db.session.add(schedule261)
    db.session.add(schedule262)
    db.session.add(schedule263)
    db.session.add(schedule264)
    db.session.add(schedule265)
    db.session.add(schedule266)
    db.session.add(schedule267)
    db.session.add(schedule268)
    db.session.add(schedule269)
    db.session.add(schedule270)
    db.session.add(schedule271)
    db.session.add(schedule272)
    db.session.add(schedule273)
    db.session.add(schedule274)
    db.session.add(schedule275)
    db.session.add(schedule276)
    db.session.add(schedule277)
    db.session.add(schedule278)
    db.session.add(schedule279)
    db.session.add(schedule280)
    db.session.add(schedule281)
    db.session.add(schedule282)
    db.session.add(schedule283)
    db.session.add(schedule284)
    db.session.add(schedule285)
    db.session.add(schedule286)
    db.session.add(schedule287)
    db.session.add(schedule288)
    db.session.add(schedule289)
    db.session.add(schedule290)
    db.session.add(schedule291)
    db.session.add(schedule292)
    db.session.add(schedule293)
    db.session.add(schedule294)
    db.session.add(schedule295)
    db.session.add(schedule296)
    db.session.add(schedule297)
    db.session.add(schedule298)
    db.session.add(schedule299)
    db.session.add(schedule300)
    db.session.add(schedule301)
    db.session.add(schedule302)
    db.session.add(schedule303)
    db.session.add(schedule304)
    db.session.add(schedule305)
    db.session.add(schedule306)
    db.session.add(schedule307)
    db.session.add(schedule308)
    db.session.add(schedule309)
    db.session.add(schedule310)
    db.session.add(schedule311)
    db.session.add(schedule312)
    db.session.add(schedule313)
    db.session.add(schedule314)
    db.session.add(schedule315)
    db.session.add(schedule316)
    db.session.add(schedule317)
    db.session.add(schedule318)
    db.session.add(schedule319)
    db.session.add(schedule320)
    db.session.add(schedule321)
    db.session.add(schedule322)
    db.session.add(schedule323)
    db.session.add(schedule324)
    db.session.add(schedule325)
    db.session.add(schedule326)
    db.session.add(schedule327)
    db.session.add(schedule328)
    db.session.add(schedule329)
    db.session.add(schedule330)
    db.session.add(schedule331)
    db.session.add(schedule332)
    db.session.add(schedule333)
    db.session.add(schedule334)
    db.session.add(schedule335)
    db.session.add(schedule336)
    db.session.add(schedule337)
    db.session.add(schedule338)
    db.session.add(schedule339)
    db.session.add(schedule340)
    db.session.add(schedule341)
    db.session.add(schedule342)
    db.session.add(schedule343)
    db.session.add(schedule344)
    db.session.add(schedule345)
    db.session.add(schedule346)
    db.session.add(schedule347)
    db.session.add(schedule348)
    db.session.add(schedule349)
    db.session.add(schedule350)
    db.session.add(schedule351)
    db.session.add(schedule352)
    db.session.add(schedule353)
    db.session.add(schedule354)
    db.session.add(schedule355)
    db.session.add(schedule356)
    db.session.add(schedule357)
    db.session.add(schedule358)
    db.session.add(schedule359)
    db.session.add(schedule360)
    db.session.add(schedule361)
    db.session.add(schedule362)
    db.session.add(schedule363)
    db.session.add(schedule364)
    db.session.add(schedule365)
    db.session.add(schedule366)
    db.session.add(schedule367)
    db.session.add(schedule368)
    db.session.add(schedule369)
    db.session.add(schedule370)
    db.session.add(schedule371)
    db.session.add(schedule372)
    db.session.add(schedule373)
    db.session.add(schedule374)
    db.session.add(schedule375)
    db.session.add(schedule376)
    db.session.add(schedule377)
    db.session.add(schedule378)
    db.session.add(schedule379)
    db.session.add(schedule380)
    db.session.add(schedule381)
    db.session.add(schedule382)
    db.session.add(schedule383)
    db.session.add(schedule384)
    db.session.add(schedule385)
    db.session.add(schedule386)
    db.session.add(schedule387)
    db.session.add(schedule388)
    db.session.add(schedule389)
    db.session.add(schedule390)
    db.session.add(schedule391)
    db.session.add(schedule392)
    db.session.add(schedule393)
    db.session.add(schedule394)
    db.session.add(schedule395)
    db.session.add(schedule396)
    db.session.add(schedule397)
    db.session.add(schedule398)
    db.session.add(schedule399)
    db.session.add(schedule400)
    db.session.add(schedule401)
    db.session.add(schedule402)
    db.session.add(schedule403)
    db.session.add(schedule404)
    db.session.add(schedule405)
    db.session.add(schedule406)
    db.session.add(schedule407)
    db.session.add(schedule408)
    db.session.add(schedule409)
    db.session.add(schedule410)
    db.session.add(schedule411)
    db.session.add(schedule412)
    db.session.add(schedule413)
    db.session.add(schedule414)
    db.session.add(schedule415)
    db.session.add(schedule416)
    db.session.add(schedule417)
    db.session.add(schedule418)
    db.session.add(schedule419)
    db.session.add(schedule420)
    db.session.add(schedule421)
    db.session.add(schedule422)
    db.session.add(schedule423)
    db.session.add(schedule424)
    db.session.add(schedule425)
    db.session.add(schedule426)
    db.session.add(schedule427)
    db.session.add(schedule428)
    db.session.add(schedule429)
    db.session.add(schedule430)
    db.session.add(schedule431)
    db.session.add(schedule432)
    db.session.add(schedule433)
    db.session.add(schedule434)
    db.session.add(schedule435)
    db.session.add(schedule436)
    db.session.add(schedule437)
    db.session.add(schedule438)
    db.session.add(schedule439)
    db.session.add(schedule440)
    db.session.add(schedule441)
    db.session.add(schedule442)
    db.session.add(schedule443)
    db.session.add(schedule444)
    db.session.add(schedule445)
    db.session.add(schedule446)
    db.session.add(schedule447)
    db.session.add(schedule448)
    db.session.add(schedule449)
    db.session.add(schedule450)
    db.session.add(schedule451)
    db.session.add(schedule452)
    db.session.add(schedule453)
    db.session.add(schedule454)
    db.session.add(schedule455)
    db.session.add(schedule456)
    db.session.add(schedule457)
    db.session.add(schedule458)
    db.session.add(schedule459)
    db.session.add(schedule460)
    db.session.add(schedule461)
    db.session.add(schedule462)
    db.session.add(schedule463)
    db.session.add(schedule464)
    db.session.add(schedule465)
    db.session.add(schedule466)
    db.session.add(schedule467)
    db.session.add(schedule468)
    db.session.add(schedule469)
    db.session.add(schedule470)
    db.session.add(schedule471)
    db.session.add(schedule472)
    db.session.add(schedule473)
    db.session.add(schedule474)
    db.session.add(schedule475)
    db.session.add(schedule476)
    db.session.add(schedule477)
    db.session.add(schedule478)
    db.session.add(schedule479)
    db.session.add(schedule480)
    db.session.add(schedule481)
    db.session.add(schedule482)
    db.session.add(schedule483)
    db.session.add(schedule484)
    db.session.add(schedule485)
    db.session.add(schedule486)
    db.session.add(schedule487)
    db.session.add(schedule488)
    db.session.add(schedule489)
    db.session.add(schedule490)
    db.session.add(schedule491)
    db.session.add(schedule492)
    db.session.add(schedule493)
    db.session.add(schedule494)
    db.session.add(schedule495)
    db.session.add(schedule496)
    db.session.add(schedule497)
    db.session.add(schedule498)
    db.session.add(schedule499)
    db.session.add(schedule500)
    db.session.add(schedule501)
    db.session.add(schedule502)
    db.session.add(schedule503)
    db.session.add(schedule504)
    db.session.add(schedule505)
    db.session.add(schedule506)
    db.session.add(schedule507)
    db.session.add(schedule508)
    db.session.add(schedule509)
    db.session.add(schedule510)
    db.session.add(schedule511)
    db.session.add(schedule512)
    db.session.add(schedule513)
    db.session.add(schedule514)
    db.session.add(schedule515)
    db.session.add(schedule516)
    db.session.add(schedule517)
    db.session.add(schedule518)
    db.session.add(schedule519)
    db.session.add(schedule520)
    db.session.add(schedule521)
    db.session.add(schedule522)
    db.session.add(schedule523)
    db.session.add(schedule524)
    db.session.add(schedule525)
    db.session.add(schedule526)
    db.session.add(schedule527)
    db.session.add(schedule528)
    db.session.add(schedule529)
    db.session.add(schedule530)
    db.session.add(schedule531)
    db.session.add(schedule532)
    db.session.add(schedule533)
    db.session.add(schedule534)
    db.session.add(schedule535)
    db.session.add(schedule536)
    db.session.add(schedule537)
    db.session.add(schedule538)
    db.session.add(schedule539)
    db.session.add(schedule540)
    db.session.add(schedule541)
    db.session.add(schedule542)
    db.session.add(schedule543)
    db.session.add(schedule544)
    db.session.add(schedule545)
    db.session.add(schedule546)
    db.session.add(schedule547)
    db.session.add(schedule548)
    db.session.add(schedule549)
    db.session.add(schedule550)
    db.session.add(schedule551)
    db.session.add(schedule552)
    db.session.add(schedule553)
    db.session.add(schedule554)
    db.session.add(schedule555)
    db.session.add(schedule556)
    db.session.add(schedule557)
    db.session.add(schedule558)
    db.session.add(schedule559)
    db.session.add(schedule560)
    db.session.add(schedule561)
    db.session.add(schedule562)
    db.session.add(schedule563)
    db.session.add(schedule564)
    db.session.add(schedule565)
    db.session.add(schedule566)
    db.session.add(schedule567)
    db.session.add(schedule568)
    db.session.add(schedule569)
    db.session.add(schedule570)
    db.session.add(schedule571)
    db.session.add(schedule572)
    db.session.add(schedule573)
    db.session.add(schedule574)
    db.session.add(schedule575)
    db.session.add(schedule576)
    db.session.add(schedule577)
    db.session.add(schedule578)
    db.session.add(schedule579)
    db.session.add(schedule580)
    db.session.add(schedule581)
    db.session.add(schedule582)
    db.session.add(schedule583)
    db.session.add(schedule584)
    db.session.add(schedule585)
    db.session.add(schedule586)
    db.session.add(schedule587)
    db.session.add(schedule588)
    db.session.add(schedule589)
    db.session.add(schedule590)
    db.session.add(schedule591)
    db.session.add(schedule592)
    db.session.add(schedule593)
    db.session.add(schedule594)
    db.session.add(schedule595)
    db.session.add(schedule596)
    db.session.add(schedule597)
    db.session.add(schedule598)
    db.session.add(schedule599)
    db.session.add(schedule600)
    db.session.add(schedule601)
    db.session.add(schedule602)
    db.session.add(schedule603)
    db.session.add(schedule604)
    db.session.add(schedule605)
    db.session.add(schedule606)
    db.session.add(schedule607)
    db.session.add(schedule608)
    db.session.add(schedule609)
    db.session.add(schedule610)
    db.session.add(schedule611)
    db.session.add(schedule612)
    db.session.add(schedule613)
    db.session.add(schedule614)
    db.session.add(schedule615)
    db.session.add(schedule616)
    db.session.add(schedule617)
    db.session.add(schedule618)
    db.session.add(schedule619)
    db.session.add(schedule620)
    db.session.add(schedule621)
    db.session.add(schedule622)
    db.session.add(schedule623)
    db.session.add(schedule624)
    db.session.add(schedule625)
    db.session.add(schedule626)
    db.session.add(schedule627)
    db.session.add(schedule628)
    db.session.add(schedule629)
    db.session.add(schedule630)
    db.session.add(schedule631)
    db.session.add(schedule632)
    db.session.add(schedule633)
    db.session.add(schedule634)
    db.session.add(schedule635)
    db.session.add(schedule636)
    db.session.add(schedule637)
    db.session.add(schedule638)
    db.session.add(schedule639)
    db.session.add(schedule640)
    db.session.add(schedule641)
    db.session.add(schedule642)
    db.session.add(schedule643)
    db.session.add(schedule644)
    db.session.add(schedule645)
    db.session.add(schedule646)
    db.session.add(schedule647)
    db.session.add(schedule648)
    db.session.add(schedule649)
    db.session.add(schedule650)
    db.session.add(schedule651)
    db.session.add(schedule652)
    db.session.add(schedule653)
    db.session.add(schedule654)
    db.session.add(schedule655)
    db.session.add(schedule656)
    db.session.add(schedule657)
    db.session.add(schedule658)
    db.session.add(schedule659)
    db.session.add(schedule660)
    db.session.add(schedule661)
    db.session.add(schedule662)
    db.session.add(schedule663)
    db.session.add(schedule664)
    db.session.add(schedule665)
    db.session.add(schedule666)
    db.session.add(schedule667)
    db.session.add(schedule668)
    db.session.add(schedule669)
    db.session.add(schedule670)
    db.session.add(schedule671)
    db.session.add(schedule672)
    db.session.add(schedule673)
    db.session.add(schedule674)
    db.session.add(schedule675)
    db.session.add(schedule676)
    db.session.add(schedule677)
    db.session.add(schedule678)
    db.session.add(schedule679)
    db.session.add(schedule680)
    db.session.add(schedule681)
    db.session.add(schedule682)
    db.session.add(schedule683)
    db.session.add(schedule684)
    db.session.add(schedule685)
    db.session.add(schedule686)
    db.session.add(schedule687)
    db.session.add(schedule688)
    db.session.add(schedule689)
    db.session.add(schedule690)
    db.session.add(schedule691)
    db.session.add(schedule692)
    db.session.add(schedule693)
    db.session.add(schedule694)
    db.session.add(schedule695)
    db.session.add(schedule696)
    db.session.add(schedule697)
    db.session.add(schedule698)
    db.session.add(schedule699)
    db.session.add(schedule700)
    db.session.add(schedule701)
    db.session.add(schedule702)
    db.session.add(schedule703)
    db.session.add(schedule704)
    db.session.add(schedule705)
    db.session.add(schedule706)
    db.session.add(schedule707)
    db.session.add(schedule708)
    db.session.add(schedule709)
    db.session.add(schedule710)
    db.session.add(schedule711)
    db.session.add(schedule712)
    db.session.add(schedule713)
    db.session.add(schedule714)
    db.session.add(schedule715)
    db.session.add(schedule716)
    db.session.add(schedule717)
    db.session.add(schedule718)
    db.session.add(schedule719)
    db.session.add(schedule720)
    db.session.add(schedule721)
    db.session.add(schedule722)
    db.session.add(schedule723)
    db.session.add(schedule724)
    db.session.add(schedule725)
    db.session.add(schedule726)
    db.session.add(schedule727)
    db.session.add(schedule728)
    db.session.add(schedule729)
    db.session.add(schedule730)
    db.session.add(schedule731)
    db.session.add(schedule732)
    db.session.add(schedule733)
    db.session.add(schedule734)
    db.session.add(schedule735)
    db.session.add(schedule736)
    db.session.add(schedule737)
    db.session.add(schedule738)
    db.session.add(schedule739)
    db.session.add(schedule740)
    db.session.add(schedule741)
    db.session.add(schedule742)
    db.session.add(schedule743)
    db.session.add(schedule744)
    db.session.add(schedule745)
    db.session.add(schedule746)
    db.session.add(schedule747)
    db.session.add(schedule748)
    db.session.add(schedule749)
    db.session.add(schedule750)
    db.session.add(schedule751)
    db.session.add(schedule752)
    db.session.add(schedule753)
    db.session.add(schedule754)
    db.session.add(schedule755)
    db.session.add(schedule756)
    db.session.add(schedule757)
    db.session.add(schedule758)
    db.session.add(schedule759)
    db.session.add(schedule760)
    db.session.add(schedule761)
    db.session.add(schedule762)
    db.session.add(schedule763)
    db.session.add(schedule764)
    db.session.add(schedule765)
    db.session.add(schedule766)
    db.session.add(schedule767)
    db.session.add(schedule768)
    db.session.add(schedule769)
    db.session.add(schedule770)
    db.session.add(schedule771)
    db.session.add(schedule772)
    db.session.add(schedule773)
    db.session.add(schedule774)
    db.session.add(schedule775)
    db.session.add(schedule776)
    db.session.add(schedule777)
    db.session.add(schedule778)
    db.session.add(schedule779)
    db.session.add(schedule780)
    db.session.add(schedule781)
    db.session.add(schedule782)
    db.session.add(schedule783)
    db.session.add(schedule784)
    db.session.add(schedule785)
    db.session.add(schedule786)
    db.session.add(schedule787)
    db.session.add(schedule788)
    db.session.add(schedule789)
    db.session.add(schedule790)
    db.session.add(schedule791)
    db.session.add(schedule792)
    db.session.add(schedule793)
    db.session.add(schedule794)
    db.session.add(schedule795)
    db.session.add(schedule796)
    db.session.add(schedule797)
    db.session.add(schedule798)
    db.session.add(schedule799)
    db.session.add(schedule800)
    db.session.add(schedule801)
    db.session.add(schedule802)
    
    #Adding suits
    suit1=Suits("SID001","M","S","Jacket",True)
    suit2=Suits("SID002","M","S","Jacket",True)
    suit3=Suits("SID003","M","S","Jacket",True)
    suit4=Suits("SID004","M","S","Jacket",True)
    suit5=Suits("SID005","M","M","Jacket",True)
    suit6=Suits("SID006","M","M","Jacket",True)
    suit7=Suits("SID007","M","M","Jacket",True)
    suit8=Suits("SID008","M","M","Jacket",True)
    suit9=Suits("SID009","M","M","Jacket",True)
    suit10=Suits("SID010","M","M","Jacket",True)
    suit11=Suits("SID011","M","M","Jacket",True)
    suit12=Suits("SID012","M","M","Jacket",True)
    suit13=Suits("SID013","M","M","Jacket",True)
    suit14=Suits("SID014","M","L","Jacket",True)
    suit15=Suits("SID015","M","L","Jacket",True)
    suit16=Suits("SID016","M","L","Jacket",True)
    suit17=Suits("SID017","M","L","Jacket",True)
    suit18=Suits("SID018","M","L","Jacket",True)
    suit19=Suits("SID019","M","L","Jacket",True)
    suit20=Suits("SID020","M","L","Jacket",True)
    suit21=Suits("SID021","M","XL","Jacket",True)
    suit22=Suits("SID022","M","XL","Jacket",True)
    suit23=Suits("SID023","M","XL","Jacket",True)
    suit24=Suits("SID024","M","XL","Jacket",True)
    suit25=Suits("SID025","M","XL","Jacket",True)
    suit26=Suits("SID026","M","XXL","Jacket",True)
    suit27=Suits("SID027","M","XXL","Jacket",True)
    suit28=Suits("SID028","M","XXL","Jacket",True)
    suit29=Suits("SID029","M","S","Pant",True)
    suit30=Suits("SID030","M","S","Pant",True)
    suit31=Suits("SID031","M","S","Pant",True)
    suit32=Suits("SID032","M","S","Pant",True)
    suit33=Suits("SID033","M","M","Pant",True)
    suit34=Suits("SID034","M","M","Pant",True)
    suit35=Suits("SID035","M","M","Pant",True)
    suit36=Suits("SID036","M","M","Pant",True)
    suit37=Suits("SID037","M","M","Pant",True)
    suit38=Suits("SID038","M","M","Pant",True)
    suit39=Suits("SID039","M","M","Pant",True)
    suit40=Suits("SID040","M","M","Pant",True)
    suit41=Suits("SID041","M","M","Pant",True)
    suit42=Suits("SID042","M","L","Pant",True)
    suit43=Suits("SID043","M","L","Pant",True)
    suit44=Suits("SID044","M","L","Pant",True)
    suit45=Suits("SID045","M","L","Pant",True)
    suit46=Suits("SID046","M","L","Pant",True)
    suit47=Suits("SID047","M","L","Pant",True)
    suit48=Suits("SID048","M","L","Pant",True)
    suit49=Suits("SID049","M","XL","Pant",True)
    suit50=Suits("SID050","M","XL","Pant",True)
    suit51=Suits("SID051","M","XL","Pant",True)
    suit52=Suits("SID052","M","XL","Pant",True)
    suit53=Suits("SID053","M","XL","Pant",True)
    suit54=Suits("SID054","M","XXL","Pant",True)
    suit55=Suits("SID055","M","XXL","Pant",True)
    suit56=Suits("SID056","M","XXL","Pant",True)
    suit57=Suits("SID057","F","S","Jacket",True)
    suit58=Suits("SID058","F","S","Jacket",True)
    suit59=Suits("SID059","F","S","Jacket",True)
    suit60=Suits("SID060","F","S","Jacket",True)
    suit61=Suits("SID061","F","M","Jacket",True)
    suit62=Suits("SID062","F","M","Jacket",True)
    suit63=Suits("SID063","F","M","Jacket",True)
    suit64=Suits("SID064","F","M","Jacket",True)
    suit65=Suits("SID065","F","M","Jacket",True)
    suit66=Suits("SID066","F","M","Jacket",True)
    suit67=Suits("SID067","F","M","Jacket",True)
    suit68=Suits("SID068","F","M","Jacket",True)
    suit69=Suits("SID069","F","M","Jacket",True)
    suit70=Suits("SID070","F","L","Jacket",True)
    suit71=Suits("SID071","F","L","Jacket",True)
    suit72=Suits("SID072","F","L","Jacket",True)
    suit73=Suits("SID073","F","L","Jacket",True)
    suit74=Suits("SID074","F","L","Jacket",True)
    suit75=Suits("SID075","F","L","Jacket",True)
    suit76=Suits("SID076","F","L","Jacket",True)
    suit77=Suits("SID077","F","XL","Jacket",True)
    suit78=Suits("SID078","F","XL","Jacket",True)
    suit79=Suits("SID079","F","XL","Jacket",True)
    suit80=Suits("SID080","F","XL","Jacket",True)
    suit81=Suits("SID081","F","XL","Jacket",True)
    suit82=Suits("SID082","F","XXL","Jacket",True)
    suit83=Suits("SID083","F","XXL","Jacket",True)
    suit84=Suits("SID084","F","XXL","Jacket",True)
    suit85=Suits("SID085","F","S","Pant",True)
    suit86=Suits("SID086","F","S","Pant",True)
    suit87=Suits("SID087","F","S","Pant",True)
    suit88=Suits("SID088","F","S","Pant",True)
    suit89=Suits("SID089","F","M","Pant",True)
    suit90=Suits("SID090","F","M","Pant",True)
    suit91=Suits("SID091","F","M","Pant",True)
    suit92=Suits("SID092","F","M","Pant",True)
    suit93=Suits("SID093","F","M","Pant",True)
    suit94=Suits("SID094","F","M","Pant",True)
    suit95=Suits("SID095","F","M","Pant",True)
    suit96=Suits("SID096","F","M","Pant",True)
    suit97=Suits("SID097","F","M","Pant",True)
    suit98=Suits("SID098","F","L","Pant",True)
    suit99=Suits("SID099","F","L","Pant",True)
    suit100=Suits("SID100","F","L","Pant",True)
    suit101=Suits("SID101","F","L","Pant",True)
    suit102=Suits("SID102","F","L","Pant",True)
    suit103=Suits("SID103","F","L","Pant",True)
    suit104=Suits("SID104","F","L","Pant",True)
    suit105=Suits("SID105","F","XL","Pant",True)
    suit106=Suits("SID106","F","XL","Pant",True)
    suit107=Suits("SID107","F","XL","Pant",True)
    suit108=Suits("SID108","F","XL","Pant",True)
    suit109=Suits("SID109","F","XL","Pant",True)
    suit110=Suits("SID110","F","XXL","Pant",True)
    suit111=Suits("SID111","F","XXL","Pant",True)
    suit112=Suits("SID112","F","XXL","Pant",True)
      
    db.session.add(suit1)          
    db.session.add(suit2)
    
    
    db.session.add(suit3)
    
    
    db.session.add(suit4)
    
    
    db.session.add(suit5)
    
    
    db.session.add(suit6)
    
    
    db.session.add(suit7)
    
    
    db.session.add(suit8)
    
    
    db.session.add(suit9)
    
    
    db.session.add(suit10)
    
    
    db.session.add(suit11)
    
    
    db.session.add(suit12)
    
    
    db.session.add(suit13)
    
    
    db.session.add(suit14)
    
    
    db.session.add(suit15)
    
    
    db.session.add(suit16)
    
    
    db.session.add(suit17)
    
    
    db.session.add(suit18)
    
    
    db.session.add(suit19)
    
    
    db.session.add(suit20)
    
    
    db.session.add(suit21)
    
    
    db.session.add(suit22)
    
    
    db.session.add(suit23)
    
    
    db.session.add(suit24)
    
    
    db.session.add(suit25)
    
    
    db.session.add(suit26)
    
    
    db.session.add(suit27)
    
    
    db.session.add(suit28)
    
    
    db.session.add(suit29)
    
    
    db.session.add(suit30)
    
    
    db.session.add(suit31)
    
    
    db.session.add(suit32)
    
    
    db.session.add(suit33)
    
    
    db.session.add(suit34)
    
    
    db.session.add(suit35)
    
    
    db.session.add(suit36)
    
    
    db.session.add(suit37)
    
    
    db.session.add(suit38)
    
    
    db.session.add(suit39)
    
    
    db.session.add(suit40)
    
    
    db.session.add(suit41)
    
    
    db.session.add(suit42)
    
    
    db.session.add(suit43)
    
    
    db.session.add(suit44)
    
    
    db.session.add(suit45)
    
    
    db.session.add(suit46)
    
    
    db.session.add(suit47)
    
    
    db.session.add(suit48)
    
    
    db.session.add(suit49)
    
    
    db.session.add(suit50)
    
    
    db.session.add(suit51)
    
    
    db.session.add(suit52)
    
    
    db.session.add(suit53)
    
    
    db.session.add(suit54)
    
    
    db.session.add(suit55)
    
    
    db.session.add(suit56)
    
    
    db.session.add(suit57)
    
    
    db.session.add(suit58)
    
    
    db.session.add(suit59)
    
    
    db.session.add(suit60)
    
    
    db.session.add(suit61)
    
    
    db.session.add(suit62)
    
    
    db.session.add(suit63)
    
    
    db.session.add(suit64)
    
    
    db.session.add(suit65)
    
    
    db.session.add(suit66)
    
    
    db.session.add(suit67)
    
    
    db.session.add(suit68)
    
    
    db.session.add(suit69)
    
    
    db.session.add(suit70)
    
    
    db.session.add(suit71)
    
    
    db.session.add(suit72)
    
    
    db.session.add(suit73)
    
    
    db.session.add(suit74)
    
    
    db.session.add(suit75)
    
    
    db.session.add(suit76)
    
    
    db.session.add(suit77)
    
    
    db.session.add(suit78)
    
    
    db.session.add(suit79)
    
    
    db.session.add(suit80)
    
    
    db.session.add(suit81)
    
    
    db.session.add(suit82)
    
    
    db.session.add(suit83)
    
    
    db.session.add(suit84)
    
    
    db.session.add(suit85)
    
    
    db.session.add(suit86)
    
    
    db.session.add(suit87)
    
    
    db.session.add(suit88)
    
    
    db.session.add(suit89)
    
    
    db.session.add(suit90)
    
    
    db.session.add(suit91)
    
    
    db.session.add(suit92)
    
    
    db.session.add(suit93)
    
    
    db.session.add(suit94)
    
    
    db.session.add(suit95)
    
    
    db.session.add(suit96)
    
    
    db.session.add(suit97)
    
    
    db.session.add(suit98)
    
    
    db.session.add(suit99)
    
    
    db.session.add(suit100)
    
    
    db.session.add(suit101)
    
    
    db.session.add(suit102)
    
    
    db.session.add(suit103)
    # 
    
    db.session.add(suit104)
    # 
    
    db.session.add(suit105)
    # 
    
    db.session.add(suit106)
    # 
    
    db.session.add(suit107)
    # 
    
    db.session.add(suit108)
    # 
    
    db.session.add(suit109)
    # 
    
    db.session.add(suit110)
    # 
    
    db.session.add(suit111)
    # 
    
    db.session.add(suit112)

    db.session.commit()   
    '''

if __name__=="__main__":    
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port,debug=True)
    #app.run(debug=True)
    



from flask import Flask, render_template, flash, request, session, url_for, redirect, jsonify
from forms import ContactForm, SignupForm, SigninForm, AvailabilityForm, CheckoutForm
from flask_mail import Message, Mail
from models import db, User, Suits, Schedule
from sqlalchemy import or_, and_, engine, table
import datetime
import os
from flask_wtf.csrf import CSRFProtect

mail = Mail()

app = Flask(__name__)

@app.route("/")
def home():
    if "email" in session:        
        user = User.query.filter_by(email = session["email"]).first()
        if user is None:
            return redirect(url_for("signin"))        
    return render_template("home.html")

@app.route("/donate")
def donate():
    return render_template("donate.html")

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "email" not in session:
        return redirect(url_for("signin"))
    user = User.query.filter_by(email = session["email"]).first()
    #print(user)
    if user is None:
        return redirect(url_for("signin"))
    elif user.email =="careerclosetatm@gmail.com":
        form = CheckoutForm()
        if request.method == "POST":
            if form.validate() == False:
                flash("All fields are required")
                return render_template("checkout.html", form=form)
            else:
                suits = Suits.query.filter(Suits.suit_id == form.suiteId.data.upper()).first()
                print suits
                if suits != None:
                    suits.available = False
                    db.session.commit()   

                return render_template("checkout.html", success = True)
        elif request.method == "GET":
            return render_template("checkout.html", form=form)  
    else:
        return render_template("home.html")
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()   
    if request.method == 'POST':
        print "post requesting"
        if form.validate() == False:       
            print "validation failed"
            for field in form: 
                for error in field.errors:
                    print(error)     
                    
            return render_template('signup.html', form=form)
        else:
            print("Creating user")   
            newuser = User(form.username.data,  form.fullname.data, form.email.data, form.uin.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()   
            session["email"] = newuser.email;
            print "signed up user"
            return redirect(url_for("home"))
   
    elif request.method == 'GET':
        print "get request"
        return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
   
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('home'))
                 
    elif request.method == 'GET':
        return render_template('signin.html', form=form)
		
@app.route('/signout')
def signout():
 
    if 'email' not in session:
        return redirect(url_for('signin'))
     
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route("/availability", methods=["GET"])
def availability():
    if "email" not in session:
        return redirect(url_for("signin"))
    user = User.query.filter_by(email = session["email"]).first()
    if user is None:
        return redirect(url_for("signin"))
    else:
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
        

@app.route('/echo/', methods=['GET'])
def echo():
    print("Entered echo")
    #form = ScheduleForm()
    date = request.args.get('date')
    print("Querying")
    #slots = Schedule.query.filter(Schedule.date == date).first()
    slots = Schedule.query.filter(Schedule.date == date).first()
    print("Finished Querying")
    return jsonify(slots = {"date":slots.date, "time9_00":slots.time9_00})    

    
@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/appointment")
def appointment():
    if "email" not in session:
        return redirect(url_for("signin"))
    user = User.query.filter_by(email = session["email"]).first()
    if user is None:
        return redirect(url_for("signin"))
    else:          
        return render_template("appointment.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    
    if request.method == "POST":
        print("contact post")
        if form.validate() == False:
            flash("All fields are required")
            print("validate false")
            return render_template("contact.html", form=form)
        else:
            print("Going to send message")
            msg = Message(form.subject.data, sender="hussain.m@tamu.edu", recipients = ["saddamhussain4321@gmail.com"])
            msg.body = """
            From: %s <%s>
            %s
            """%(form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            print("message sent")
            return render_template("contact.html", success = True)
    elif request.method == "GET":
        print("contact get")
        return render_template("contact.html", form=form)

if __name__=="__main__":
    #app.secret_key = "12345667"
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = 'careerclosetatm@gmail.com'
    app.config["MAIL_PASSWORD"] = 'Group5Password'
	#wtf updated
    app.config["SECRET_KEY"] = "123456789"
    app.config["WTF_CSRF_SECRET_KEY"] = "123456789"
    app.config["WTF_CSRF_ENABLED"] = True
    mail.init_app(app)
    csrf = CSRFProtect()
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development'
    from models import db
    db.init_app(app)
    with app.test_request_context():
        #db.drop_all()
        #User.__table__.drop(engine)
        db.create_all()
#         suit1=Suits("SID001","M","S","Jacket",True)
#         suit2=Suits("SID002","M","S","Jacket",True)
#         suit3=Suits("SID003","M","S","Jacket",True)
#         suit4=Suits("SID004","M","S","Jacket",True)
#         suit5=Suits("SID005","M","M","Jacket",True)
#         suit6=Suits("SID006","M","M","Jacket",True)
#         suit7=Suits("SID007","M","M","Jacket",True)
#         suit8=Suits("SID008","M","M","Jacket",True)
#         suit9=Suits("SID009","M","M","Jacket",True)
#         suit10=Suits("SID010","M","M","Jacket",True)
#         suit11=Suits("SID011","M","M","Jacket",True)
#         suit12=Suits("SID012","M","M","Jacket",True)
#         suit13=Suits("SID013","M","M","Jacket",True)
#         suit14=Suits("SID014","M","L","Jacket",True)
#         suit15=Suits("SID015","M","L","Jacket",True)
#         suit16=Suits("SID016","M","L","Jacket",True)
#         suit17=Suits("SID017","M","L","Jacket",True)
#         suit18=Suits("SID018","M","L","Jacket",True)
#         suit19=Suits("SID019","M","L","Jacket",True)
#         suit20=Suits("SID020","M","L","Jacket",True)
#         suit21=Suits("SID021","M","XL","Jacket",True)
#         suit22=Suits("SID022","M","XL","Jacket",True)
#         suit23=Suits("SID023","M","XL","Jacket",True)
#         suit24=Suits("SID024","M","XL","Jacket",True)
#         suit25=Suits("SID025","M","XL","Jacket",True)
#         suit26=Suits("SID026","M","XXL","Jacket",True)
#         suit27=Suits("SID027","M","XXL","Jacket",True)
#         suit28=Suits("SID028","M","XXL","Jacket",True)
#         suit29=Suits("SID029","M","S","Pant",True)
#         suit30=Suits("SID030","M","S","Pant",True)
#         suit31=Suits("SID031","M","S","Pant",True)
#         suit32=Suits("SID032","M","S","Pant",True)
#         suit33=Suits("SID033","M","M","Pant",True)
#         suit34=Suits("SID034","M","M","Pant",True)
#         suit35=Suits("SID035","M","M","Pant",True)
#         suit36=Suits("SID036","M","M","Pant",True)
#         suit37=Suits("SID037","M","M","Pant",True)
#         suit38=Suits("SID038","M","M","Pant",True)
#         suit39=Suits("SID039","M","M","Pant",True)
#         suit40=Suits("SID040","M","M","Pant",True)
#         suit41=Suits("SID041","M","M","Pant",True)
#         suit42=Suits("SID042","M","L","Pant",True)
#         suit43=Suits("SID043","M","L","Pant",True)
#         suit44=Suits("SID044","M","L","Pant",True)
#         suit45=Suits("SID045","M","L","Pant",True)
#         suit46=Suits("SID046","M","L","Pant",True)
#         suit47=Suits("SID047","M","L","Pant",True)
#         suit48=Suits("SID048","M","L","Pant",True)
#         suit49=Suits("SID049","M","XL","Pant",True)
#         suit50=Suits("SID050","M","XL","Pant",True)
#         suit51=Suits("SID051","M","XL","Pant",True)
#         suit52=Suits("SID052","M","XL","Pant",True)
#         suit53=Suits("SID053","M","XL","Pant",True)
#         suit54=Suits("SID054","M","XXL","Pant",True)
#         suit55=Suits("SID055","M","XXL","Pant",True)
#         suit56=Suits("SID056","M","XXL","Pant",True)
#         suit57=Suits("SID057","F","S","Jacket",True)
#         suit58=Suits("SID058","F","S","Jacket",True)
#         suit59=Suits("SID059","F","S","Jacket",True)
#         suit60=Suits("SID060","F","S","Jacket",True)
#         suit61=Suits("SID061","F","M","Jacket",True)
#         suit62=Suits("SID062","F","M","Jacket",True)
#         suit63=Suits("SID063","F","M","Jacket",True)
#         suit64=Suits("SID064","F","M","Jacket",True)
#         suit65=Suits("SID065","F","M","Jacket",True)
#         suit66=Suits("SID066","F","M","Jacket",True)
#         suit67=Suits("SID067","F","M","Jacket",True)
#         suit68=Suits("SID068","F","M","Jacket",True)
#         suit69=Suits("SID069","F","M","Jacket",True)
#         suit70=Suits("SID070","F","L","Jacket",True)
#         suit71=Suits("SID071","F","L","Jacket",True)
#         suit72=Suits("SID072","F","L","Jacket",True)
#         suit73=Suits("SID073","F","L","Jacket",True)
#         suit74=Suits("SID074","F","L","Jacket",True)
#         suit75=Suits("SID075","F","L","Jacket",True)
#         suit76=Suits("SID076","F","L","Jacket",True)
#         suit77=Suits("SID077","F","XL","Jacket",True)
#         suit78=Suits("SID078","F","XL","Jacket",True)
#         suit79=Suits("SID079","F","XL","Jacket",True)
#         suit80=Suits("SID080","F","XL","Jacket",True)
#         suit81=Suits("SID081","F","XL","Jacket",True)
#         suit82=Suits("SID082","F","XXL","Jacket",True)
#         suit83=Suits("SID083","F","XXL","Jacket",True)
#         suit84=Suits("SID084","F","XXL","Jacket",True)
#         suit85=Suits("SID085","F","S","Pant",True)
#         suit86=Suits("SID086","F","S","Pant",True)
#         suit87=Suits("SID087","F","S","Pant",True)
#         suit88=Suits("SID088","F","S","Pant",True)
#         suit89=Suits("SID089","F","M","Pant",True)
#         suit90=Suits("SID090","F","M","Pant",True)
#         suit91=Suits("SID091","F","M","Pant",True)
#         suit92=Suits("SID092","F","M","Pant",True)
#         suit93=Suits("SID093","F","M","Pant",True)
#         suit94=Suits("SID094","F","M","Pant",True)
#         suit95=Suits("SID095","F","M","Pant",True)
#         suit96=Suits("SID096","F","M","Pant",True)
#         suit97=Suits("SID097","F","M","Pant",True)
#         suit98=Suits("SID098","F","L","Pant",True)
#         suit99=Suits("SID099","F","L","Pant",True)
#         suit100=Suits("SID100","F","L","Pant",True)
#         suit101=Suits("SID101","F","L","Pant",True)
#         suit102=Suits("SID102","F","L","Pant",True)
#         suit103=Suits("SID103","F","L","Pant",True)
#         suit104=Suits("SID104","F","L","Pant",True)
#         suit105=Suits("SID105","F","XL","Pant",True)
#         suit106=Suits("SID106","F","XL","Pant",True)
#         suit107=Suits("SID107","F","XL","Pant",True)
#         suit108=Suits("SID108","F","XL","Pant",True)
#         suit109=Suits("SID109","F","XL","Pant",True)
#         suit110=Suits("SID110","F","XXL","Pant",True)
#         suit111=Suits("SID111","F","XXL","Pant",True)
#         suit112=Suits("SID112","F","XXL","Pant",True)
#              
#         db.session.add(suit1)          
#         db.session.add(suit2)
#           
#          
#         db.session.add(suit3)
#         
#         
#         db.session.add(suit4)
#         
#         
#         db.session.add(suit5)
#         
#         
#         db.session.add(suit6)
#         
#         
#         db.session.add(suit7)
#         
#         
#         db.session.add(suit8)
#         
#         
#         db.session.add(suit9)
#         
#         
#         db.session.add(suit10)
#         
#         
#         db.session.add(suit11)
#         
#         
#         db.session.add(suit12)
#         
#         
#         db.session.add(suit13)
#         
#         
#         db.session.add(suit14)
#         
#         
#         db.session.add(suit15)
#         
#         
#         db.session.add(suit16)
#         
#         
#         db.session.add(suit17)
#         
#         
#         db.session.add(suit18)
#         
#         
#         db.session.add(suit19)
#         
#         
#         db.session.add(suit20)
#         
#         
#         db.session.add(suit21)
#         
#         
#         db.session.add(suit22)
#         
#         
#         db.session.add(suit23)
#         
#         
#         db.session.add(suit24)
#         
#         
#         db.session.add(suit25)
#         
#         
#         db.session.add(suit26)
#         
#         
#         db.session.add(suit27)
#         
#         
#         db.session.add(suit28)
#         
#         
#         db.session.add(suit29)
#         
#         
#         db.session.add(suit30)
#         
#         
#         db.session.add(suit31)
#         
#         
#         db.session.add(suit32)
#         
#         
#         db.session.add(suit33)
#         
#         
#         db.session.add(suit34)
#         
#         
#         db.session.add(suit35)
#         
#         
#         db.session.add(suit36)
#         
#         
#         db.session.add(suit37)
#         
#         
#         db.session.add(suit38)
#         
#         
#         db.session.add(suit39)
#         
#         
#         db.session.add(suit40)
#         
#         
#         db.session.add(suit41)
#         
#         
#         db.session.add(suit42)
#         
#         
#         db.session.add(suit43)
#         
#         
#         db.session.add(suit44)
#         
#         
#         db.session.add(suit45)
#         
#         
#         db.session.add(suit46)
#         
#         
#         db.session.add(suit47)
#         
#         
#         db.session.add(suit48)
#         
#         
#         db.session.add(suit49)
#         
#         
#         db.session.add(suit50)
#         
#         
#         db.session.add(suit51)
#         
#         
#         db.session.add(suit52)
#         
#         
#         db.session.add(suit53)
#         
#         
#         db.session.add(suit54)
#         
#         
#         db.session.add(suit55)
#         
#         
#         db.session.add(suit56)
#         
#         
#         db.session.add(suit57)
#         
#         
#         db.session.add(suit58)
#         
#         
#         db.session.add(suit59)
#         
#         
#         db.session.add(suit60)
#         
#         
#         db.session.add(suit61)
#         
#         
#         db.session.add(suit62)
#         
#         
#         db.session.add(suit63)
#         
#         
#         db.session.add(suit64)
#         
#         
#         db.session.add(suit65)
#         
#         
#         db.session.add(suit66)
#         
#         
#         db.session.add(suit67)
#         
#         
#         db.session.add(suit68)
#         
#         
#         db.session.add(suit69)
#         
#         
#         db.session.add(suit70)
#         
#         
#         db.session.add(suit71)
#         
#         
#         db.session.add(suit72)
#         
#         
#         db.session.add(suit73)
#         
#         
#         db.session.add(suit74)
#         
#         
#         db.session.add(suit75)
#         
#         
#         db.session.add(suit76)
#         
#         
#         db.session.add(suit77)
#         
#         
#         db.session.add(suit78)
#         
#         
#         db.session.add(suit79)
#         
#         
#         db.session.add(suit80)
#         
#         
#         db.session.add(suit81)
#         
#         
#         db.session.add(suit82)
#         
#         
#         db.session.add(suit83)
#         
#         
#         db.session.add(suit84)
#         
#         
#         db.session.add(suit85)
#         
#         
#         db.session.add(suit86)
#         
#         
#         db.session.add(suit87)
#         
#         
#         db.session.add(suit88)
#         
#         
#         db.session.add(suit89)
#         
#         
#         db.session.add(suit90)
#         
#         
#         db.session.add(suit91)
#         
#         
#         db.session.add(suit92)
#         
#         
#         db.session.add(suit93)
#         
#         
#         db.session.add(suit94)
#         
#         
#         db.session.add(suit95)
#         
#         
#         db.session.add(suit96)
#         
#         
#         db.session.add(suit97)
#         
#         
#         db.session.add(suit98)
#         
#         
#         db.session.add(suit99)
#         
#         
#         db.session.add(suit100)
#         
#         
#         db.session.add(suit101)
#         
#         
#         db.session.add(suit102)
#         
#         
#         db.session.add(suit103)
#         # 
#         
#         db.session.add(suit104)
#         # 
#         
#         db.session.add(suit105)
#         # 
#         
#         db.session.add(suit106)
#         # 
#         
#         db.session.add(suit107)
#         # 
#         
#         db.session.add(suit108)
#         # 
#         
#         db.session.add(suit109)
#         # 
#         
#         db.session.add(suit110)
#         # 
#         
#         db.session.add(suit111)
#         # 
#         
#         db.session.add(suit112)
#         db.session.commit()
#           
#         schedule1 = Schedule(datetime.datetime.strptime('19-03-17', '%d-%m-%y').date(),'1','1','1','1','1','1''1','1','1','1')
#         schedule2 = Schedule(datetime.datetime.strptime('20-03-17', '%d-%m-%y').date(),'0','1','0','1','0','1''0','1','0','1')
#         schedule3 = Schedule(datetime.datetime.strptime('21-03-17', '%d-%m-%y').date(),'1','1','0','1','1','0''1','1','0','1')
#         db.session.add(schedule1)
#         db.session.add(schedule2)
#         db.session.add(schedule3)
#         
#          
#         suit1 = Suits('400','m','s','jacket',True)
#         suit2 = Suits('2','m','s','jacket')
#         suit3 = Suits('3','m','s','jacket')
#         suit4 = Suits('4','m','m','jacket')
#         suit5 = Suits('5','m','m','jacket')
#         suit6 = Suits('6','m','l','jacket')
#         suit7 = Suits('7','m','s','pant')
#         suit8 = Suits('8','m','m','pant')
#         suit9 = Suits('9','m','l','pant')
#                     
#         suit10 = Suits('10','f','s','jacket')
#         suit11 = Suits('11','f','m','jacket')
#         suit12 = Suits('12','f','m','jacket')
#         suit13 = Suits('13','f','m','jacket')
#         suit14 = Suits('14','f','l','jacket')
#         suit15 = Suits('15','f','l','jacket')
#         suit16 = Suits('16','f','l','jacket')
#         suit17 = Suits('17','f','s','pant')
#         suit18 = Suits('18','f','m','pant')
#         suit19 = Suits('19','f','l','pant')
#         db.session.add(suit1)
#          
#         db.session.add(suit2)
#          
#         db.session.add(suit3)
#          
#         db.session.add(suit4)
#          
#         db.session.add(suit5)
#          
#         db.session.add(suit6)
#          
#         db.session.add(suit7)
#          
#         db.session.add(suit8)
#          
#         db.session.add(suit9)
#          
#         db.session.add(suit10)
#          
#         db.session.add(suit11)
#          
#         db.session.add(suit12)
#          
#         db.session.add(suit13)
#          
#         db.session.add(suit14)
#          
#         db.session.add(suit15)
#          
#         db.session.add(suit16)
#          
#         db.session.add(suit17)
#          
#         db.session.add(suit18)
#          
#         db.session.add(suit19)
#         
#           


#         
        #Creating Suits DB
        
        
    
    
    
            
            
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port,debug=True)
    


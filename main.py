from flask import Flask,request,jsonify
import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash,generate_password_hash
import uuid
import jwt
import os

app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']='THEPASSCODE1'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    public_id=db.Column(db.String(50),unique=True)
    name=db.Column(db.String(50))
    password=db.Column(db.String(80))
    email=db.Column(db.String(80),unique=True)
    admin=db.Column(db.Boolean)
    sensor=db.relationship('Sensor',backref='user',uselist=False)
   

    def __init__(self,public_id,name,password,email,admin):
        self.public_id=public_id
        self.name=name
        self.email=email
        self.password=password
        self.admin=admin

class Sensor(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.String(50),db.ForeignKey('user.public_id'))
    Height=db.Column(db.Float)
    weight=db.Column(db.Float)
    Bmp=db.Column(db.Float)
    Temp=db.Column(db.Float)
    def __init__(self,Height,weight,Bmp,Temp,user_id):
        self.Height=Height
        self.weight=weight
        self.Bmp=Bmp
        self.Temp=Temp
        self.user_id=user_id
        

class Doctor(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    field=db.Column(db.String(50))
  


class Nurse(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    Nurse_id=db.Column(db.String(50),unique=True)
   

class Patient(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    Patient_id=db.Column(db.String(50),unique=True)
 

class Appointment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.String(50))
    description=db.Column(db.String(50))
    
    
    






@app.route('/',methods=['GET'])
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route("/api/user",methods=['POST'])
def create_user():
    data=request.get_json() 
    name=data["name"]
    email=data["email"]
    password=data['password']
    print("name:",name,"email:",email,"password:",password)
    hashed_password=generate_password_hash(password,method='sha256')
    new_user=User(public_id=str(uuid.uuid4()),name=name,password=hashed_password,email=email,admin=False)
    try:

      
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'status':201,
            "msg":"New user created"
        }),201
    
    except:
        return jsonify({'status':404,
            'msg':"email already exist"
        }),404


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

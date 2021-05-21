#import numpy as np
from flask import Flask, request, jsonify, render_template, redirect
import pickle
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from random import randint

app = Flask(__name__)
model = pickle.load(open('nb_model.pkl', 'rb'))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
#DATABSE_URI='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='your_user', password='password', server='localhost', database='dname')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/covid'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/Covid'
db= SQLAlchemy(app)

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='xyz@gmail.com'
app.config['MAIL_PASSWORD']='password'                    #you have to give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
otp=randint(000000,999999)

class Users(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.Text, nullable=False)
    email= db.Column(db.String(50), unique=True, nullable=False)
    password= db.Column(db.String(100), nullable=False)


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/validate', methods=['GET', 'POST'])
def validate():
    if request.method=='POST':
        user_otp=request.form['otp']
        if otp==int(user_otp):
            return redirect('/predict')
        else:
            output= "Invalid Otp, Please enter valid otp"
            return render_template('validate_otp.html', valid_text='{}'.format(output))
    return render_template('validate_otp.html')

@app.route('/register', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        name= request.form.get('name')
        email= request.form.get('email')
        password= request.form.get('password')
        msg=Message(subject='OTP',sender='covid_checker@gmail.com',recipients=[email])
        msg.body=str(otp)
        mail.send(msg)

        entry= Users(name=name, email=email, password=password)
        db.session.add(entry)
        db.session.commit()
        return redirect('/validate')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email= request.form.get('email')
        password= request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        #User.query.filter(User.email.endswith('@example.com')).all()
        if password == user.password:
            return render_template('index.html')

    return render_template('login.html')


@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
        features = [int(x) for x in request.form.values()]
        #print("xxxxx" + str(features))
        #final_features = [np.array(int_features)]
        #final_features = [list(int_features)]
        print(features)
        prediction = model.predict([features])

        output = prediction[0]
        #print("yyyyy" + str(output))
        if output==1:
            output= "Disease may be Covid"
            
        elif output==0:
            output= "Disease is not Covid"
        return render_template('index.html', prediction_text='{}'.format(output))
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

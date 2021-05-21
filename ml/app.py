#import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
model = pickle.load(open('model1.pkl', 'rb'))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
#DATABSE_URI='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='your_user', password='password', server='localhost', database='dname')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/covid'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/Covid'
db= SQLAlchemy(app)

class Users(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.Text, nullable=False)
    email= db.Column(db.String(50), unique=True, nullable=False)
    password= db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        name= request.form.get('name')
        email= request.form.get('email')
        password= request.form.get('password')
        entry= Users(name=name, email=email, password=password)
        db.session.add(entry)
        db.session.commit()
        return render_template('index.html')
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


@app.route('/predict',methods=['POST'])
def predict():

    int_features = [int(x) for x in request.form.values()]
    #final_features = [np.array(int_features)]
    #final_features = [list(int_features)]
    #prediction = model.predict(final_features)

    output = prediction[0]

    return render_template('index.html', prediction_text='Disease maybe {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)

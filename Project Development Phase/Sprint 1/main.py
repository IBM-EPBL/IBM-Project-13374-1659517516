from flask import Flask, render_template, request,redirect,session, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import mysql.connector
import os
import pickle
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key=os.urandom(24)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'liver'

mysql = MySQL(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register/')
def about():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'email' in session:
        return render_template('form.html')
    else:
        return redirect('/')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    if mysql:
        print("Connection Successful!")
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT * FROM `user_details` where `email` LIKE '{}' and `password` LIKE '{}'""".format(email, password))
        users = cursor.fetchall()
        cursor.close()
    else:
        print("Connection Failed!")

    if len(users)>0:
        session['email'] = users[0][1]
        return redirect('/home')
    else:
        return redirect('/')
    return "Success"

@app.route('/add_user',methods=['POST'])
def add_user():
    username=request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    occupation = request.form.get('occupation')
    phone = request.form.get('phone')
    if mysql:
        print("Connection Successful!")
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO `user_details` (`username`,`email`,`phone`,`occupation`,`password`) VALUES ('{}','{}','{}','{}','{}')""".format(username,email, phone,occupation,password))
        mysql.connection.commit()
        cursor.close()
    else:
        print("Connection Failed!")
    return "User Registered Successfully."


@app.route('/logout')
def logout():
    session.pop('email')
    return redirect('/')
@app.route('/form',methods=['POST'])
def form():
    print("HOME")
    return redirect('form.html')
@app.route('/predict', methods=['POST'])
def predict():

    age = request.form['age']
    gender = request.form['gender']
    tb = request.form['tb']
    dbi = request.form['dbi']
    ap = request.form['ap']
    aa1 = request.form['aa1']
    aa2 = request.form['aa2']
    tp = request.form['tp']
    a = request.form['a']
    agr = request.form['agr']
    if gender == "Male":
        gender = 1
    else:
        gender = 0
    data = [[float(age),
            float(gender),
            float(tb),
            float(dbi),
            float(ap),
            float(aa1),
            float(aa2),
            float(tp),
            float(a),
            float(agr)]]

    model = pickle.load(open('liver1.pkl', 'rb'))

    prediction = model.predict(data)
    if (prediction == 1):
        return render_template('noChance.html',
                               prediction='You don\'t have disease.')
    else:
        return render_template('chance.html',
                               prediction='Oops.You have Liver Disease.')



if __name__=="__main__":
    app.run(debug=True)



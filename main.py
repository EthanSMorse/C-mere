from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

conn = pymysql.connect(
    database="emorse_",
    user="emorse",
    password="228246286",
    host="10.100.33.60",
    cursorclass= pymysql.cursors.DictCursor
)

@app.route('/')
def index ():
    return render_template("home.html.jinja")

@app.route('/registration',  methods=['GET', 'POST'])
def registration ():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO `User`(`Username`, `Passwords`, `Email`) VALUES ('{username}', '{password}', '{email}')")
        cursor.close()
        conn.commit()
        return redirect('/signin')
    return render_template("registration.html.jinja")

@app.route('/signin',  methods=['GET', 'POST'])
def signup ():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `User` WHERE `Username` = '{username}'")
        user = cursor.fetchone()
        cursor.close()
        conn.commit()
        if user["Password"] == password:
            return redirect('/feed')


    return render_template("signin.html.jinja")

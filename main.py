from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login

app = Flask(__name__)
app.secret_key = "UR7XLL009"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def get_id(self):
        return str(self.id)
    
@login_manager.user_loader
def load_user(user_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM `User` WHERE `id` = {user_id}")
    result = cursor.fetchone()
    cursor.close()
    conn.commit()

    if result is None:
        return None
    
    return User(result["ID"], result["Username"], result["Email"])



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
        result = cursor.fetchone()
        cursor.close()
        conn.commit()
        if result["Password"] == password:
            user = load_user(result['ID'])
            flask_login.login_user(user)

            return redirect('/feed')

    return render_template("signin.html.jinja")

@app.route('/feed')

@flask_login.login_required

def post_feed():
    return 'feed page'
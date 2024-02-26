from flask import Flask, render_template, request, redirect, g
import pymysql
import pymysql.cursors
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

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="emorse",
        password="228246286",
        database="emorse_",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close()

@login_manager.user_loader
def load_user(user_id):
    cursor = get_db().cursor()
    cursor.execute(f"SELECT * FROM `User` WHERE `id` = {user_id}")
    result = cursor.fetchone()
    cursor.close()
    get_db().commit()

    if result is None:
        return None
    
    return User(result["ID"], result["Username"], result["Email"])

@app.route('/')
def index ():
    return render_template("home.html.jinja")

@app.route('/registration',  methods=['GET', 'POST'])
def registration ():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `User`(`Username`, `Password`, `Email`) VALUES ('{username}', '{password}', '{email}')")
        cursor.close()
        get_db().commit()
        return redirect('/signin')
    return render_template("registration.html.jinja")

@app.route('/signin',  methods=['GET', 'POST'])
def signup ():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        cursor = get_db().cursor()
        cursor.execute(f"SELECT * FROM `User` WHERE `Username` = '{username}'")
        result = cursor.fetchone()
        cursor.close()
        get_db().commit()
        if result["Password"] == password:
            user = load_user(result['ID'])
            flask_login.login_user(user)

            return redirect('/feed')

    return render_template("signin.html.jinja")

@app.route('/feed', methods=['GET', 'POST'])
@flask_login.login_required
def post_feed():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM `Posts` INNER JOIN `User` ON `Posts`.user_id = `User`.ID ORDER BY `timestamp` DESC")
    results = cursor.fetchall()
    cursor.close()
    return render_template("feed.html.jinja", posts = results)
    return flask_login.current_user

@app.route('/post', methods=['GET', 'POST'])
@flask_login.login_required
def post():
    description = request.form['description']
    user_id = flask_login.current_user.id
    cursor = get_db().cursor()
    cursor.execute(f"INSERT INTO `Posts` (`description`, `user_id`) VALUES ('{description}', '{user_id}')")
    cursor.close()
    get_db().commit
    return redirect("/feed")


from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index ():
    return render_template("home.html.jinja")

@app.route('/registration')
def registration ():
    return render_template("registration.html.jinja")

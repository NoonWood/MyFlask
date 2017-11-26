from flask import render_template, flash, redirect
from app import app
#from forms import LoginForm

@app.route('/')
def homepage():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/index')
def index():
    user = {'nickname': 'User'}
    posts = [
        {
            'author':{'nickname':'Gregory'},
            'body':'Welcome for my kurs project !'
        }
    ]

    return render_template("index.html",
                           title = "Home",
                           user = user,
                           posts = posts)
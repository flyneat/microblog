from webapp import app
from flask import render_template, flash, redirect, url_for, request
from webapp.forms import LoginForm


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    data = request.data
    user = {'name': 'zpf'}
    title = 'Home'
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title=title, user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login request for user: {form.username.data}, remember_me: {form.remember_me.data}')
        return redirect(url_for('login'))
    return render_template('login.html', form=form, title='登录')

from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app, bcrypt, db


# dummy data to demonstrate Jinja in HTML templates
title_string = "Conor's Flask App"
example_blogs = [
    {'author': "Conor Waldron",
     'title': 'How to build a tennis dash app',
     'content': 'dash is really useful to make web apps that you can deploy with docker on AWS...',
     'date_posted': '20th Nov 2023'},
    {'author': "Leo Kavanagh",
     'title': 'Functional Programming',
     'content': 'Functional Programming is like making a tirimisu...',
     'date_posted': '16th Feb 2022'},
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=example_blogs, title=title_string)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # if you are already logged in you cant re-register
        flash('You are already logged in, you cant re-register until you sign out', 'danger')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # only save encrypted passwords to database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # if you are already logged in you cant re-login
        flash('You are already logged in, you cant re-login until you sign out', 'danger')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # the fields meet the minimum requirements, lets check do the details match any users in our db
        # check if that email exists
        with app.app_context():
            existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user: # is that email in our system?
            if bcrypt.check_password_hash(existing_user.password, form.password.data): # is password correct
                # success, log them in
                login_user(existing_user, remember=form.remember.data)
                flash(f'Login successful for {form.email.data}', 'success')
                return redirect(url_for('home'))
            else: #invalid password
                flash('Login Unsuccessful. Please check email and password', 'danger')
        else: # email not recognised
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('Successfuly logged out', 'success')
    return redirect(url_for('home'))
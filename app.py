from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' # should be replaced with environment variable later


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'conor.waldron@optum.com' and form.password.data == '123':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
if __name__ == '__main__':
    app.run(debug=True)
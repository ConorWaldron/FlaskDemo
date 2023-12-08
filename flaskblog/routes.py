from flask import render_template, url_for, flash, redirect, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flaskblog import app, bcrypt, db

"""
# dummy data to demonstrate Jinja in HTML templates
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
"""

@app.route('/')
@app.route('/home')
def home():
    #read posts from database, note we dont need to use app.app_contex() as we are in Flask
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title="Conor's Flask App")

@app.route('/about')
def about():
    return render_template('about.html', title='About')

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
        # check if that email exists, note we dont need app.app_context from within flask
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

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():  # update username and email
        # apparently app.app_context() not needed here, although it wont work for me, with or without app.app_context
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account details have been updated', 'success')
        return redirect(url_for('account'))

    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        a_new_post=Post(title=form.title.data, content=form.post_content.data, author=current_user)
        db.session.add(a_new_post)
        db.session.commit()
        flash('Post successfully published!', 'success')
        return redirect(url_for('home'))
    return render_template('create_edit_post.html', title='New Post', form=form,
                           heading_title='Create Post')

# the <int:variable_name> syntax enforces the variable to be an int
@app.route("/post/<int:post_id>")
def post(post_id):
    this_post = Post.query.get_or_404(post_id)
    # below we are passing in key value pairs as arguments to be used in the HTML
    return render_template('post.html', title=this_post.title, post=this_post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    this_post = Post.query.get_or_404(post_id)
    # check that only the author of the post can update the post
    if this_post.author != current_user:
        abort(403)

    form = PostForm()
    if request.method == 'GET':
        # auto populate form with existing data
        form.title.data = this_post.title
        form.post_content.data = this_post.content
    elif request.method == 'POST':
        # update database
        if form.validate_on_submit():
            this_post.title = form.title.data
            this_post.content = form.post_content.data
            db.session.commit() # note we dont need an add as the data is already there
            flash('Your post was successfully updated', 'success')
            return redirect(url_for('post', post_id=this_post.id))

    return render_template('create_edit_post.html', title='Edit Post', form=form,
                           heading_title='Update Post')

@app.route("/post/<int:post_id>/delete")
@login_required
def delete_post(post_id):
    this_post = Post.query.get_or_404(post_id)
    # check that only the author of the post can delete the post
    if this_post.author != current_user:
        abort(403)
    else:
        # delete post
        db.session.delete(this_post)
        db.session.commit()
        flash('Your post was successfully deleted', 'success')
        return redirect(url_for('home', post_id=this_post.id))

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


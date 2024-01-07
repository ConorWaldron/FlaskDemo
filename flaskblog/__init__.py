from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
#flaskblog.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' # should be replaced with environment variable later
app.config['SECRET_KEY'] = os.environ.get('FLASK_DEMO_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # name of the route that does login
login_manager.login_message_category = 'info' # make message pretty

# warning, you need this import after making db, as the routes module imports db from flask
# so you want to prevent a circular reference
from flaskblog import routes

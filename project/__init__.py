from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
# from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)

if os.environ.get('ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/warbler-db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# toolbar = DebugToolbarExtension(app)

modus = Modus(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

from project.users.views import users_blueprint
from project.messages.views import messages_blueprint
from project.users.models import User
from project.messages.models import Message
from flask_login import current_user

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(
    messages_blueprint, url_prefix='/users/<int:id>/messages')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def root():
    if current_user.is_authenticated:
        followees = current_user.following.all()
        if len(followees):
            ids = [f.id for f in followees] + [current_user.id]
            messages = Message.query.filter(
                Message.user_id.in_(ids)).order_by("timestamp desc").limit(100)
        else:
            messages = Message.query.order_by("timestamp desc").limit(100)
        return render_template('home.html', messages=messages)
    return render_template('home.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

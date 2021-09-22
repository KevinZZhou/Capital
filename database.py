from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'google.login'

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
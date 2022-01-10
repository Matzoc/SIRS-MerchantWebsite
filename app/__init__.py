from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from functools import wraps

import os
db = SQLAlchemy()


def admin_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role != "admin":
            return "rip", 401
        
        return f(*args, **kwargs)
        
    return wrap


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usr:password@'+ os.environ["host"] +'/test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '1234'#FIXME give me a real secret key
    db.init_app(app)

    from .models import init
    init(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


#add tries to everything(!)

#sessions
#   session cookie
#   make the website remember you are logged in
#   account levels

#Account menu
#   change password - later
#   order history - later
#   shop cart - later
#   ?

#Shop
#   shop page
#   page to add custom items to the shop (the admin accounts can do this)
#   store purchases in database


#Order Page
#
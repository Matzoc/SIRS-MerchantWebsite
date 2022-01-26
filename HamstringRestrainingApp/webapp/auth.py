from flask import Flask, render_template, request, make_response, redirect, url_for
from flask import Blueprint
from argon2 import PasswordHasher
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db, get_user_role
from .messages import login_msgs, register_msgs
from secrets import token_urlsafe
from datetime import datetime


auth = Blueprint('auth', __name__)
ph = PasswordHasher()    


def verify_register(email, password):
    user = User.query.filter_by(email=email).first()

    if user:
        return False
    else:
        hashed_password = ph.hash(password)
        token = token_urlsafe(32)

        from .mail import send_verification
        send_verification(email, url_for("auth.verify_email", token = token, _external = True))
    
        new_user = User(email = email, password = hashed_password, role = "unverified", token = token, timestamp = datetime.utcnow())

        db.session.add(new_user)
        db.session.commit()
        
        return True


@auth.route('/register')
def register():
    return render_template('register.html', role = get_user_role())


@auth.route('/register', methods = ['POST'])
def register_post():
    email, password = request.form.get("email"), request.form.get("password")

    if not verify_register(email, password):
        return render_template("register.html", msg = register_msgs["error"], role = get_user_role(), msg_type = "error")
    else:
        return render_template("register.html", msg = register_msgs["success"], role = get_user_role(), msg_type = "success")


@auth.route('/verify_email/<token>', methods = ['GET'])
def verify_email(token):
    user = User.query.filter_by(token=token).first()

    if user and user.token == token and (datetime.utcnow() - user.timestamp).total_seconds() < 120 * 60:
        user.token = None
        user.role = "default"

        db.session.commit()

        return render_template('verify_email.html', role = get_user_role())
    else:
        return "Page not found", 400




@auth.route('/login')
def login():
    return render_template("login.html", role = get_user_role())


@auth.route('/login', methods = ['POST'])
def login_post():
    email, password = request.form.get("email"), request.form.get("password")
    user = User.query.filter_by(email=email).first()
    msg = login_msgs["error"]

    if not user:
        msg = login_msgs["wrong password"] 
        return render_template("login.html", msg = msg, msg_type = "error", role = get_user_role())

    if user.role == 'unverified':
        msg = login_msgs["account not verified"] 
        return render_template("login.html", msg = msg, msg_type = "error", role = get_user_role())


    try:
        ph.verify(user.password, password)
        login_user(user, remember=False)

        return redirect(url_for('main.profile'))
    except:
        msg = login_msgs["wrong password"] 
        return render_template("login.html", msg = msg, msg_type = "error", role = get_user_role())

    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.landing'))
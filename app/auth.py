from flask import Flask, render_template, request, make_response, redirect, url_for
from flask import Blueprint
from argon2 import PasswordHasher
from flask_login import login_user
from .models import User
from . import db
import base64


auth = Blueprint('auth', __name__)
ph = PasswordHasher()


def verify_register(email, password):
    user = User.query.filter_by(email=email).first()

    if user:
        return False
    else:
        hashed_password = ph.hash(password)
        new_user = User(email=email, password = hashed_password, role = "default")
        db.session.add(new_user)
        db.session.commit()
        
        return True


@auth.route('/register')
def register():
    return render_template('register.html')


@auth.route('/register', methods = ['POST'])
def register_post():
    email, password = request.form.get("email"), request.form.get("password")

    if not verify_register(email, password):
        return render_template("register.html", error_msg = "email already in use")
    else:
        return render_template("register.html", error_msg = "we did it wee")


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/login', methods = ['POST'])
def login_post():
    email, password = request.form.get("email"), request.form.get("password")
    user = User.query.filter_by(email=email).first()

    if user and ph.verify(user.password, password):
        login_user(user, remember=False)
        return redirect(url_for('main.profile'))
    
    return render_template("login.html", error_msg = "login failed, please try again")

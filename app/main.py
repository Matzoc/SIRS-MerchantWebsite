from flask import Blueprint
from flask import Flask, render_template, request, make_response
from flask_login import login_required, current_user
from functools import wraps
from . import admin_login_required

main = Blueprint('main', __name__)


@main.route('/')
def landing():
    return render_template("index.html")


@main.route('/profile')
@login_required
def profile():
    return render_template('account.html')


@main.route('/admin')
@login_required
@admin_login_required
def admin():
    return render_template('account.html')

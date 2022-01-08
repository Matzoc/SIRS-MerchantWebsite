from flask import Flask, render_template, request, make_response
import account
import os

app = Flask(__name__)

account.init(os.environ["host"])


@app.route('/')
def landing():
    return render_template("marketplace.html", catalog = ["test", "test2", "test3"])
    return render_template("index.html")


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        email, password = request.form.get("email"), request.form.get("password")

        print("email: " + email)
        if not account.register_account(email, password):
            return render_template("register.html", error_msg = "email already in use")
        else:
            return render_template("register.html", error_msg = "we did it wee")
    else:
        return render_template("register.html")


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        email, password = request.form.get("email"), request.form.get("password")

        if account.login_account(email, password):
            response = make_response(render_template("account.html"))     
            response.set_cookie("auth", value='thisIsAValue')
            
            return response
        
        
        return render_template("login.html", error_msg = "login failed, please try again")
    else:
        return render_template("login.html")


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
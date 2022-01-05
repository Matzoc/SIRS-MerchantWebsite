from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'


@app.route('/')
def landing():
    return render_template("index.html")


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        email, password = request.form.get("email"), request.form.get("password")

        print("email: " + email)
        if not register_account(email, password):
            return render_template("register.html", error_msg = "email already in use")
        else:
            return render_template("register.html", error_msg = "we did it wee")
    else:
        return render_template("register.html")


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        email, password = request.form.get("email"), request.form.get("password")

        if login_account(email, password):
            render_template("account.html")
        else:
            render_template("login.html", error_msg = "login failed, please try again")
    else:
        return render_template("register.html")






#Login page
#Register Page

#Account menu
#Shop


#Order Menu
#
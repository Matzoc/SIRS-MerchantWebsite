from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import os
import MySQLdb.cursors


app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ["host"]
app.config['MYSQL_USER'] = "usr"
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

def testDB():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * from users''')
    rv = cursor.fetchall()

    return (str(rv))

@app.route('/')
def landing():
    return testDB()
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
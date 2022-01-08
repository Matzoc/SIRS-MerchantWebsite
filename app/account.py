from argon2 import PasswordHasher
import argon2
import base64
import mysql.connector
import mysql
ph = PasswordHasher()


class Account:
    def __init__(self, email, password):
        self.email = ""
        self.password = password #very safe, obviously change this

    def __eq__(self, other):
        return self.email == other.email

    def login(self, password):
        return self.password == password

    
class DefaultAccount(Account):
    def __init__(self, email, password):
        Account.__init__(email, password)


def register_account(email, password):
    password_hash = ph.hash(password.encode('ascii'))
    cursor = db_connection.cursor()
    cursor.execute(''' SELECT email FROM users WHERE email = %s''', (email,))
    result = cursor.fetchall()

    if len(result) != 0:
        return "Registration failed, email already in use. Please login instead."
        
    #make it insert base64 encoded values
    cursor.execute('''INSERT INTO users VALUES (%s, %s)''', (email, password_hash))
    db_connection.commit()    

    return True
    

def login_account(email, password):
    cursor = db_connection.cursor()

    cursor.execute(''' SELECT email, password_hash FROM users WHERE email = %s''', (email,))
    result = cursor.fetchall()

    if len(result) < 1:
        return False

    try:
        return ph.verify(result[0][1], password)
    except argon2.exceptions.VerifyMismatchError:
        return False



class Product:
    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description


def init(host):
    global db_connection 
    db_connection = mysql.connector.connect(host=host, user="usr", password="password", database="test")

    
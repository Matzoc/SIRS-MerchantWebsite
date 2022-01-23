from flask import Flask
from flask_mail import Mail, Message

mail = Mail()

def init(app):
    settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": 'hamstringrestraining@gmail.com',
        "MAIL_PASSWORD": "-5v+nPGRrpm6cuEZ",
        "MAIL_DEFAULT_SENDER" : 'hamstringrestraining@gmail.com' 
    }

    app.config.update(settings)
    mail.init_app(app)


def send_verification(email, token):
    msg = Message(subject="Hello",
                recipients=[email], # replace with your email for testing
                body="Click this link to verify your account: " + token)
    mail.send(msg)
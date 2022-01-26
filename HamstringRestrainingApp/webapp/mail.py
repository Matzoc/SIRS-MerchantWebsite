import smtplib, ssl


def send_verification(email, token):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "hamstringrestraining@gmail.com"  # Enter your address
    receiver_email = email  # Enter receiver address
    password = "-5v+nPGRrpm6cuEZ"
    message = """\
    Subject: Hi there\n

    Click this link to verify your account: : %s""" % (token)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
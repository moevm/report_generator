from flask_mail import Mail

MAIL = None


def getMail():
    global MAIL
    if MAIL is None:
        MAIL = Mail()
    return MAIL
from app import app
from services.mail_service import getMail
from flask_mail import Message
from flask import render_template

HEADER_LETTER = 'Access to Report Generator'
MAIL_SERVER = 'MAIL_SERVER'


class Mail:

    mail_username = "test_report_generator@mail.ru"
    mail_password = 'passwordrepo'

    def configure_mail(self):
        mail_settings = {
            "MAIL_SERVER": "smtp.mail.ru",
            "MAIL_USE_SSL": True,
            "MAIL_USERNAME": self.mail_username,
            "MAIL_PORT": 465,
            "MAIL_PASSWORD": self.mail_password,
            "MAIL_USE_TLS": False
        }

        app.config.update(mail_settings)
        mail = getMail()
        mail.init_app(app)

    def __init__(self):
        if MAIL_SERVER not in app.config:
            self.configure_mail()

    def get_message(self, email):
        msg = Message(HEADER_LETTER,
                      sender=self.mail_username,
                      recipients=[email])

        msg.html = render_template('letter.html')

        return msg

    def send_message(self, email):
        msg = self.get_message(email)
        mail = getMail()
        mail.send(msg)

import smtplib
from email.mime.text import MIMEText

class NotifierClient:
    def __init__(self, settings):
        self.port = 587
        self.smtp_server = 'smtp.gmail.com'
        self.settings = settings
    def send_email(self, **kwargs):
        body = kwargs.get('body')
        subject = kwargs.get('subject')
        message = MIMEText(body)
        message['Subject'] = subject
        with smtplib.SMTP(self.smtp_server, port=self.port) as connection:
            connection.starttls()
            connection.login(user=self.settings.notifier.SMTP_USER_OUTGOING_EMAIL, password=self.settings.SMTP_USER_OUTGOING_EMAIL_APP_PASS)
            connection.send_message(from_addr=self.settings.notifier.SMTP_USER_OUTGOING_EMAIL, to_addrs=self.settings.notifier.SMTP_USER_RECEIVING_EMAIL,msg=message)


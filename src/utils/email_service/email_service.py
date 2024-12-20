import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.username = os.getenv('SMTP_USERNAME')
        self.password = os.getenv('SMTP_PASSWORD')
        self.use_tls = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'
      

    def send_email(self, to: str, subject: str, message: str):
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                msg = MIMEMultipart()
                msg['From'] = self.username
                msg['To'] = to
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))
                server.send_message(msg)
        except Exception as e:
            raise Exception(f"Error al enviar el correo: {e}")

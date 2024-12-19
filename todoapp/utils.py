import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
import os
from dotenv import load_dotenv

load_dotenv()

sender_email_env = os.getenv('SENDER_EMAIL')
sender_password_env = ' '.join(os.getenv('SENDER_PASSWORD').split(','))
smtp_server_env = os.getenv('SENDER_SMTP_SEVER')

def generate_code():
    return str(str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)))


def send_verification_code(email, code, email_goal, email_main):
    sender_email = sender_email_env
    sender_password = sender_password_env
    smtp_server = smtp_server_env
    smtp_port = 587
    
    with open('todoapp/email.html', 'r') as file:
        html_template = file.read()

    # Replace the placeholder with the actual code
    html_message = html_template.replace('{{ code }}', code).replace('{{ email_goal }}', email_goal).replace('{{ email_main }}', email_main)
    

    # Email subject and message
    subject = 'Verification Code'
    plain_message = f'Your verification code is: {code}'

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject

    # Attach both plain text and HTML versions
    msg.attach(MIMEText(plain_message, 'plain'))
    msg.attach(MIMEText(html_message, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")
        return None

    return code

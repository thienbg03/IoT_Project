import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def send_email_notification():
    # Email server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = 'cevelinevangelista@gmail.com'
    password = 'lmjc rlei pmmt ngwu'

    # Email content
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    subject = "Light Notification"
    body = f"The Light is ON at {current_time}."

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = 'cevelinevangelista@gmail.com'
    msg['Subject'] = subject

    # Attach email body
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, 'cevelinevangelista@gmail.com', msg.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')

# email.py
import smtplib

def send_email(recipient_email, temperature):
    subject='Temperature Warning'
    body = f'The current temperature is {temperature}. Would you like to turn on the fan?'
    
    try:
        # Email configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 465
        sender_email = 'santisinsight@gmail.com'  # Replace with your email
        sender_password = 'dtgu jzjx qlwk oopn'   # Replace with your password

        # Email content
        message = f'Subject: {subject}\n\n{body}'

        # Send the email
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message)
        server.quit()

        print('Email sent successfully!')
        return True
    except Exception as e:
        print(f'Failed to send email. Error: {e}')
        return False

import email
import imaplib
import smtplib
from uuid import uuid4

sender_email = 'santisinsight@gmail.com'
sender_password = 'vyhx wkam hrli olmr'
server = 'imap.gmail.com'

# Dictionary to track processed responses for each session
session_responses = {}

# Create a new session ID for each email sent
current_session_id = None

def send_email(recipient_email, temperature):
    global current_session_id
    current_session_id = str(uuid4())  # Generate a new session ID
    session_responses[current_session_id] = set()  # Initialize empty set for this session

    subject = 'Temperature Warning'
    body = f'The current temperature is {temperature}. Would you like to turn on the fan?'

    try:
        # Email configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 465

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

def receive_email():
    print("Receive email method is being called from email.py")
    global current_session_id

    if not current_session_id:
        print('No email session is currently active.')
        return False

    # Connect to the server and login
    mail = imaplib.IMAP4_SSL(server)
    mail.login(sender_email, sender_password)
    mail.select('inbox')

    # Search for unread emails
    status, data = mail.search(None, 'UNSEEN')
    mail_ids = data[0].split()

    if not mail_ids:
        print('No new emails found.')
        return False

    # Process each unread email
    for mail_id in mail_ids:
        status, data = mail.fetch(mail_id, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_subject = message['subject']

                if message.is_multipart():
                    for part in message.walk():
                        if part.get_content_type() == 'text/plain':
                            mail_content = part.get_payload(decode=True).decode()
                else:
                    mail_content = message.get_payload(decode=True).decode()

                # Extract email address from 'from' field
                sender_address = mail_from.split('<')[-1].strip('>')

                # Check if the sender's email has already responded in this session
                if sender_address in session_responses[current_session_id]:
                    print(f'Response from {sender_address} already processed for this session. Ignoring.')
                    continue

                # Process the email content
                print(f'From: {mail_from}')
                print(f'Subject: {mail_subject}')
                print(f'Content: {mail_content.strip()}')

                if "yes" in mail_content.lower():
                    session_responses[current_session_id].add(sender_address)  # Mark as processed
                    return True
                elif "no" in mail_content.lower():
                    session_responses[current_session_id].add(sender_address)  # Mark as processed

    return False

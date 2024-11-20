# email.py
import email
import imaplib
import smtplib

sender_email = 'santisinsight@gmail.com'
sender_password = 'vyhx wkam hrli olmr'
server = 'imap.gmail.com'

def send_email(recipient_email, temperature):
    subject='Temperature Warning'
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

                # Print for debugging
                print(f'From: {mail_from}')
                print(f'Subject: {mail_subject}')
                print(f'Content: {mail_content.strip()}')

                if "yes" in mail_content.lower():
                    return True

    return False

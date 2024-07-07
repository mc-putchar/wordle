#!.venv/bin/python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    mail.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: astavrop <astavrop@student.42berlin.de>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/06 16:30:09 by astavrop          #+#    #+#              #
#    Updated: 2024/07/06 16:32:12 by astavrop         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# > Every program attempts to expand until it can read mail.
# > Those programs which cannot so expand are replaced by ones which can.
# -- James Zawinski, 1995

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import imaplib
import email
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

class EmailClient:
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.imap_server = 'imap.gmail.com'
        self.username = os.getenv('EMAIL_USER')
        self.password = os.getenv('APP_PASS')

    def send_email(self, to_address, subject, body, body_type='plain', attachment=None):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_address
        msg['Subject'] = subject

        # Add the body of the email
        msg.attach(MIMEText(body, body_type))

        # Add the attachment if there is one
        if attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attachment, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
            msg.attach(part)

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, to_address, msg.as_string())
            server.close()
            print(f'Email sent to {to_address}')
        except Exception as e:
            print(f'Failed to send email: {e}')

    def receive_emails(self, folder='inbox', search_criteria='ALL'):
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.username, self.password)
        mail.select(folder)

        result, data = mail.search(None, search_criteria)
        email_ids = data[0].split()

        emails = []
        for email_id in email_ids:
            result, message_data = mail.fetch(email_id, '(RFC822)')
            raw_email = message_data[0][1].decode('utf-8')
            email_message = email.message_from_string(raw_email)

            emails.append({
                'from': email_message['from'],
                'subject': email_message['subject'],
                'body': self._get_body(email_message)
                })

        mail.logout()
        return emails

    def _get_body(self, email_message):
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode('utf-8')
        else:
            return email_message.get_payload(decode=True).decode('utf-8')

client = EmailClient()

body = ""
with open("./templates/default.html", "r") as file:
    body = ''.join(e for e in file.readlines())

print(body)

# Send an email
client.send_email(
    to_address='sung-hle@student.42berlin.de',
    subject='Laws of Software',
    body=body,
    body_type='html'
)

# Receive emails
# emails = client.receive_emails()
# for email in emails:
#     print(type(email))
#     print(json.dumps(email))
#     print()

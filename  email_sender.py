import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
from config import SMTP_CONFIG

# Setup logging
logging.basicConfig(filename='email_sender.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def send_email(subject, body, to_email, from_email, password, file_path=None):
    try:
        # Setup the MIME
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach file if provided
        if file_path:
            attach_file(msg, file_path)

        # Connect to SMTP server
        with smtplib.SMTP(SMTP_CONFIG['server'], SMTP_CONFIG['port']) as server:
            server.starttls()  # Secure the connection
            server.login(from_email, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)

        logging.info(f"Email sent successfully to {to_email}")

    except smtplib.SMTPAuthenticationError:
        logging.error("Authentication Error: Unable to log in.")
        print("Authentication error. Please check your credentials.")
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        print(f"Error occurred: {str(e)}")

def attach_file(msg, file_path):
    try:
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(file_path)}")
            msg.attach(part)
        logging.info(f"Attached file: {file_path}")
    except Exception as e:
        logging.error(f"Error attaching file: {str(e)}")
        print(f"Error occurred while attaching the file: {str(e)}")

if __name__ == "__main__":
    from_email = 'your_email@gmail.com'
    to_email = 'recipient_email@gmail.com'
    password = 'your_app_password'  # Use app password if 2FA is enabled
    subject = 'Test Email with Attachment'
    body = 'This is a test email sent from Python!'
    file_path = 'path_to_your_attachment'  # Optional: Provide a file path or leave it None

    send_email(subject, body, to_email, from_email, password, file_path)

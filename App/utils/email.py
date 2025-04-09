import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

# Original function: https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/


# Load environment variables from .flaskenv or .env
load_dotenv()


def send_email(receiver_email: str, subject: str, body: str):
    """
    Sends an email via the Gmail SMTP server using TLS protocols.
    """
    print(f"Attempting to send email to {receiver_email}...")
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)

    try:
        # Host and port info: https://support.google.com/a/answer/176600?hl=en
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(sender_email, sender_password)
            s.sendmail(sender_email, receiver_email, body)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

import os
import smtplib
from dotenv import load_dotenv

# Original function: https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/


# Load environment variables from .flaskenv or .env
load_dotenv()


def send_email(receiver_email: str, message: str):
    print(f"Attempting to send email to {receiver_email}...")
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(sender_email, sender_password)
            s.sendmail(sender_email, receiver_email, message)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

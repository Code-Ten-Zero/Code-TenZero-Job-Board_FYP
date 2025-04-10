import os
import smtplib
from email.message import EmailMessage
from flask import render_template


def send_email(recipient_email: str, subject: str, template_name: str, message: str = "", **kwargs) -> bool:
    """
    Sends an email with both plain text and HTML content using Jinja2 templates.

    Args:
        recipient_email (str): Recipient's email address.
        subject (str): Subject of the email.
        template_name (str): Base filename of the email templates (without extension).
        message (str): Optional message content to pass to the template.
        **kwargs: Any additional variables passed into the templates.

    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    try:
        # Load credentials from environment
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")

        if not sender_email or not sender_password:
            raise EnvironmentError(
                "Missing EMAIL_USER or EMAIL_PASS in environment."
            )

        # Render email content from templates
        html_content = render_template(
            f'emails/{template_name}.html.j2', message=message, **kwargs
        )
        text_content = render_template(
            f'emails/{template_name}.txt.j2', message=message, **kwargs
        )

        # Create email message object
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg.set_content(text_content)           # Fallback text
        msg.add_alternative(html_content, subtype='html')  # HTML part

        # Send using Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        print(f"Email sent to {recipient_email}")
        return True

    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
        return False

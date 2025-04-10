import os
import smtplib
from email.message import EmailMessage
from flask import render_template, url_for

"""
====== MAIN EMAIL FUNCTION ======
"""


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


"""
====== HELPERS FOR VARIOUS TEMPLATES ======
"""


def send_job_published_email(recipient, listing, posting_company, is_company=False):
    """
    Sends an email notification when a new job listing is posted.

    This helper function wraps the `send_email` function to send a notification 
    to either the company or the alumni. It includes the job title, company name, 
    location, and a link to the job posting.

    Args:
        recipient (object): The recipient of the email (either a CompanyAccount or AlumnusAccount).
        listing (JobListing): The job listing object containing details about the job.
        posting_company (CompanyAccount): The company posting the job.
        is_company (bool): Flag to indicate if the recipient is a subscribed alumnus
            (False; default value), or the posting company (True).

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        recipient_name = None
        message = None
        subject = None
        
        if is_company:
            recipient_name = recipient.registered_name
            message = f"You job listing, {listing.title}, has been published!",
            subject = "Your Listing Has Been Published"
        else:
            recipient_name = f"{recipient.first_name} {recipient.last_name}"
            message=f"{posting_company.registered_name} posted a new job: {listing.title}",
            subject = "New Job Listing"
        
        job_url = url_for(
            'index_views.view_listing',
            listing_id=listing.id,
            _external=True
        )

        return send_email(
            recipient_email=recipient.login_email,
            template_name="job_published",
            subject=subject,
            message=message,
            recipient_name=recipient_name,
            job_title=listing.title,
            company_name=posting_company.registered_name,
            job_location=listing.location,
            job_url=job_url
        )
    except Exception as e:
        print(f"[Email Helper Error] {e}")
        return False

import os
import smtplib
from email.message import EmailMessage
from flask import render_template, url_for
from typing import Union

from App.models import (
    AlumnusAccount,
    CompanyAccount,
    JobListing
)

LISTING_PAGE_ROUTE = 'alumni_views.view_listing_page'

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


def send_job_published_email(
        recipient: Union[CompanyAccount, AlumnusAccount],
        listing: JobListing,
        posting_company: CompanyAccount
):
    """
    Sends an email notification when a job listing is published.

    Depending on the recipient type, this function customizes the message:
    - To the company that posted the job (CompanyAccount), confirming their listing is live.
    - To subscribed alumni (AlumnusAccount), informing them of the new opportunity.

    Args:
        recipient (Union[CompanyAccount, AlumnusAccount]): The email recipient.
        listing (JobListing): The job listing that was published.
        posting_company (CompanyAccount): The company responsible for posting the job.

    Returns:
        bool: True if the email was sent successfully, False otherwise.

    Raises:
        ValueError: If the recipient is not an instance of CompanyAccount or AlumnusAccount.
    """
    try:
        recipient_name = None
        message = None
        subject = None

        if isinstance(recipient, CompanyAccount):
            recipient_name = recipient.registered_name
            message = f"You job listing, {listing.title}, has been published!",
            subject = "Your Listing Has Been Published"

        elif isinstance(recipient, AlumnusAccount):
            recipient_name = f"{recipient.first_name} {recipient.last_name}"
            message = f"{posting_company.registered_name} posted a new job: {listing.title}",
            subject = "New Job Listing"
        else:
            raise ValueError(
                "Recipient must be a CompanyAccount or AlumnusAccount.")

        job_url = url_for(
            LISTING_PAGE_ROUTE,
            id=listing.id,
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
            job_location=listing.job_site_address,
            job_url=job_url
        )
    except Exception as e:
        print(f"[Email Helper Error] {e}")
        return False


def send_job_unpublished_email(
    recipient: Union[CompanyAccount, AlumnusAccount],
    listing: JobListing,
    posting_company: CompanyAccount
) -> bool:
    """
    Sends an email notification when a job listing is unpublished.

    Depending on the recipient type, this function customizes the message:
    - To the company that posted the job (CompanyAccount), notifying them their job is unpublished.
    - To subscribed alumni (AlumnusAccount), informing them the job is temporarily unavailable.

    Args:
        recipient (Union[CompanyAccount, AlumnusAccount]): The email recipient.
        listing (JobListing): The job listing that was unpublished.
        posting_company (CompanyAccount): The company that posted the job.

    Returns:
        bool: True if the email was sent successfully, False otherwise.

    Raises:
        ValueError: If the recipient is not an instance of CompanyAccount or AlumnusAccount.
    """
    try:
        if isinstance(recipient, CompanyAccount):
            recipient_name = recipient.registered_name
            message = f"Your job listing, {listing.title}, has been temporarily unpublished."
            subject = "Your Job Listing Has Been Unpublished"
        elif isinstance(recipient, AlumnusAccount):
            recipient_name = f"{recipient.first_name} {recipient.last_name}"
            message = f"The job listing {listing.title} by {posting_company.registered_name} has been temporarily unpublished."
            subject = "Job Listing Unpublished"
        else:
            raise ValueError(
                "Recipient must be a CompanyAccount or AlumnusAccount.")

        job_url = url_for(LISTING_PAGE_ROUTE,
                          listing_id=listing.id, _external=True)

        return send_email(
            recipient_email=recipient.login_email,
            template_name="job_unpublished",
            subject=subject,
            message=message,
            recipient_name=recipient_name,
            job_title=listing.title,
            company_name=posting_company.registered_name,
            job_location=listing.job_site_address,
            job_url=job_url
        )
    except Exception as e:
        print(f"[Email Helper Error] {e}")
        return False


def send_job_deleted_email(
    recipient: Union[CompanyAccount, AlumnusAccount],
    listing: JobListing,
    posting_company: CompanyAccount
) -> bool:
    """
    Sends an email notification when a job listing is deleted.

    Depending on the recipient type, this function customizes the message:
    - To the company that posted the job (CompanyAccount), confirming deletion.
    - To subscribed alumni (AlumnusAccount), informing them the listing is no longer available.

    Args:
        recipient (Union[CompanyAccount, AlumnusAccount]): The email recipient.
        listing (JobListing): The job listing that was deleted.
        posting_company (CompanyAccount): The company that posted the job.

    Returns:
        bool: True if the email was sent successfully, False otherwise.

    Raises:
        ValueError: If the recipient is not an instance of CompanyAccount or AlumnusAccount.
    """
    try:
        if isinstance(recipient, CompanyAccount):
            recipient_name = recipient.registered_name
            message = f"Your job listing, {listing.title}, has been deleted!"
            subject = "Your Listing Has Been Deleted"
        elif isinstance(recipient, AlumnusAccount):
            recipient_name = f"{recipient.first_name} {recipient.last_name}"
            message = f"The job listing {listing.title} by {posting_company.registered_name} has been deleted."
            subject = "Job Listing Deleted"
        else:
            raise ValueError(
                "Recipient must be a CompanyAccount or AlumnusAccount.")

        job_url = url_for(LISTING_PAGE_ROUTE,
                          listing_id=listing.id, _external=True)

        return send_email(
            recipient_email=recipient.login_email,
            template_name="job_deleted",
            subject=subject,
            message=message,
            recipient_name=recipient_name,
            job_title=listing.title,
            company_name=posting_company.registered_name,
            job_location=listing.job_site_address,
            job_url=job_url
        )
    except Exception as e:
        print(f"[Email Helper Error] {e}")
        return False

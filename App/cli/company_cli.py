import click
from flask.cli import AppGroup
from App.controllers.company_account import (
    add_company_account,
    get_all_company_accounts,
)

from App.controllers.job_listing import (
     get_job_listings_by_company_id,
)
company_cli = AppGroup('company', help='Company object commands')


@company_cli.command("list", help="Lists company in the database")
@click.option("--jsonify-results", is_flag=True, help="Return results in JSON format")
def list_listing_command(jsonify_results):
    print(get_all_company_accounts(jsonify_results))


@company_cli.command("add", help="Add an copmany object to the database")
@click.argument("registered_name", default="aah pull")
@click.argument("password_hash", default="password")
@click.argument("login_email", default="aahpull@mail")
@click.argument("mailing_address", default="aahpull address")
@click.argument("phone_number", default="8689009000")
@click.argument("public_email", default="aahpull@mail")
@click.argument("website_url", default="https://www.aahpull.com")
def add_company_account_command(registered_name, password, login_email, mailing_address, phone_number, public_email, website_url):
    company = add_company_account(registered_name, password, login_email,
                                  mailing_address, phone_number, public_email, website_url)

    if company is None:
        print('Error creating company')
    else:
        print(f'{company} created!')

# flask company notifications


@company_cli.command("notifications", help="Show all notifications for a company")
@click.argument("registered_name", default="company1")
def show_notifications(company_id):
    listings = get_job_listings_by_company_id (company_id)

    notifications = []

    for listing in listings:
        notifications.extend(listing.get_notifications())

    if notifications:
        for notification in notifications:
            print(
                f"Notification: {notification.message} (Timestamp: {notification.created_at})")
    else:
        print(f"No notifications found for {listings.company.registered_name}.")

from flask import Flask
from App.main import create_app
from App.database import db, get_migrate

# Import CLI command groups
from App.cli.admin_cli import admin_cli
from App.cli.alumnus_cli import alumnus_cli
from App.cli.company_cli import company_cli
from App.cli.job_listing_cli import job_listing_cli
from App.cli.user_cli import user_cli
from App.cli.test_cli import test_cli

from App.controllers.admin_account import add_admin_account
from App.controllers.alumnus_account import add_alumnus_account
from App.controllers.company_account import add_company_account
from App.controllers.job_listing import add_job_listing


app = create_app()
migrate = get_migrate(app)

# Register CLI commands
app.cli.add_command(admin_cli)
app.cli.add_command(alumnus_cli)
app.cli.add_command(company_cli)
app.cli.add_command(job_listing_cli)
app.cli.add_command(user_cli)
app.cli.add_command(test_cli)


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()

    # add in the first admin
    print("Adding debug admin account: bob@mail")
    add_admin_account('bob@mail.com', 'bobpass')

    # add in alumnus
    print("Adding debug alumnus account: rob@mail")
    add_alumnus_account(
        'rob@mail.com',
        'robpass',
        'robfname',
        'roblname',
        phone_number='1868-333-4444',
    )

    # add in companies
    print("Adding debug company account: company@mail")
    company1 = add_company_account(
        'company@mail.com',
        'compass',
        'company1',
        'mailing_address',
        'public@email',
        'company_website.com',
        'phone_number',
    )
    print("Adding debug company account: company@mail2")
    company2 = add_company_account(
        'company@mail2.com',
        'compass',
        'company2',
        'mailing_address2',
        'public2@email',
        'company_website2.com',
        'phone_number2'
    )

    # add in listings
    print("Adding debug job listing: listing1")
    add_job_listing(
        company1.id,
        'listing1',
        'Part-time',
        'job description1',
        8000,
        False,
        'Curepe'
    )
    print("Adding debug job listing: listing2")
    add_job_listing(
        company2.id,
        'listing2',
        'Full-time',
        'job description2',
        4000,
        False,
        'Port-Of-Spain'
    )
    print("Adding debug job listing: listing3")
    add_job_listing(
        company2.id,
        'listing3',
        'Full-time',
        'job description3',
        4000,
        False,
        'Port-Of-Spain'
    )
    print("Adding debug job listing: listing4")
    add_job_listing(
        company1.id,
        'listing4',
        'Full-time',
        'job description4',
        4000,
        False,
        'Port-Of-Spain'
    )

    print('database intialized')

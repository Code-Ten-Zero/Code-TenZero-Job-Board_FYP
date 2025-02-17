import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *

# #( create_user, get_all_users_json, get_all_users, get_all_admins, get_all_admins_json,
#      add_admin, add_alumni, add_company, add_listing,
#      get_all_companies, get_all_companies_json,
#      get_all_alumni, get_all_alumni_json, get_all_listings, get_all_listings_json, get_company_listings, get_all_subscribed_alumni,
#      is_alumni_subscribed, send_notification, apply_listing, get_all_applicants,
#      get_user_by_email, get_user, get_listing, delete_listing, subscribe, unsubscribe,
#      login, toggle_listing_approval, get_listing_title)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# TODO:
# HANDLE FILES!
# MAILING LIST!

# CLASS BASED AUTHENTICATION?

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    # create_user('bob', 'bobpass')

    # add in the first admin
    add_admin('bobpass', 'bob@mail')

    # add in alumni
    add_alumni('robpass', 'rob@mail', '1868-333-4444', 'robfname', 'roblname')

    # add_alumni('rooooob', 'robpass', 'roooooob@mail', '123456089')

    # add_categories('123456789', ['Database'])
    # print('test')

    # remove_categories('123456789', ['N/A'])
    # remove_categories('123456789', ['Database'])
    

    # subscribe rob
    # subscribe_action('123456789', ['Software Engineer'])

    # subscribe('123456789', 'Database Manager')
    # unsubscribe('123456789')

    

    # add in companies
    add_company('company1', 'compass', 'company@mail',  'company_address', 'public@mail', 'contact', 'company_website.com')
    add_company('company2', 'compass', 'company2@mail',  'company_address2', 'public2@mail', 'contact2', 'company_website.com')

    # add in listings
    # listing1 = add_listing('listing1', 'job description', 'company2')
    # print(listing1, 'test')
    add_listing('listing1', 'job description1', 'company1',
                8000, 'Part-time', True, True, 'desiredCandidate?', 'Curepe', ['Database Manager', 'Programming', 'butt'])

    add_listing('listing2', 'job description', 'company2',
                4000, 'Full-time', True, True, 'desiredCandidate?', 'Curepe', ['Database Manager', 'Programming', 'butt'])

    


    # print(get_all_listings_json())
    print(get_company_listings('company2'))
    

    print(get_all_subscribed_alumni())
    # send_notification(['Programming'])
    # create_user('username', 'password', 'email')
    # print(get_user_by_username('rob'))
    # print(jwt_authenticate('bob', 'bobpass'))

    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(username, password):
#     create_user(username, password)
#     print(f'{username} created!')

# this command will be : flask user create bob bobpass

# flask user list
@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

# add in command groups and commands for:
# - admin
# - alumni 
# - business 
# - listing


# admin commands
# flask admin list
admin_cli = AppGroup('admin', help='Admin object commands') 

@admin_cli.command("list", help="Lists admins in the database")
@click.argument("format", default="string")
def list_admin_command(format):
    if format == 'string':
        print(get_all_admins())
    else:
        print(get_all_admins_json())

# flask admin add
@admin_cli.command("add", help="adds an admin")
@click.argument("username", default='bob2')
@click.argument("password", default='bobpass')
@click.argument("email", default="bob@mail2")
def add_admin_command( password, email):
    admin = add_admin(password, email)
    
    if admin is None:
        print('Error creating admin')
    else:
        print(f'{admin} created')

@admin_cli.command("toggle", help="Approve or disapprove a job listing")
@click.argument("listing_id", default='1')
def toggle_approval_command(listing_id):
    result = toggle_listing_approval(listing_id)

    if result is None:
        print(f"Listing with ID {listing_id} not found or could not be approved.")
    else:
        print(f"Listing with ID {listing_id} has been {'approved' if result else 'disapproved'}.")


app.cli.add_command(admin_cli)


# alumni commands
alumni_cli = AppGroup('alumni', help='Alumni object commands')

# flask alumni list
@alumni_cli.command("list", help="Lists alumnis in the database")
@click.argument("format", default="string")
def list_alumni_command(format):
    if format == 'string':
        print(get_all_alumni())
    else:
        print(get_all_alumni_json())

# flask alumni add
@alumni_cli.command("add", help = "Add an alumni object to the database")
#@click.argument("username", default="rob2")
@click.argument("password", default="robpass")
@click.argument("email", default="rob@mail2")
@click.argument("alumni_id", default="987654321")
@click.argument("phone_number", default="8686861000")
@click.argument("firstname", default="rob2fname")
@click.argument("lastname", default="rob2lname")
# @click.argument("job_categories", default='Database')
def add_alumni_command(password, email, alumni_id, phone_number, firstname, lastname):
    alumni = add_alumni(password, email, alumni_id, phone_number, firstname, lastname)

    if alumni is None:
        print('Error creating alumni')
    else:
        print(f'{alumni} created!')

# flask alumni subscribe
# add in better error checking for subscribe_action - try except that the user exists
@alumni_cli.command("subscribe", help="Subscribe an alumni object")
@click.argument("alumni_id", default="123456789")
def subscribe_alumni_command(alumni_id):
    alumni = subscribe(alumni_id)

    if alumni is None:
        print('Error subscribing alumni')
    else:
        if is_alumni_subscribed(alumni_id):
            print(f'{alumni} subscribed!')
        else:
            print(f'{alumni} unsubscribed!')

# flask alumni add_categories
# note, must manually add in job_categories in the cli command eg: flask alumni add_categories 123456789 Database,Programming
@alumni_cli.command("add_categories", help="Add job categories for the user")
@click.argument("alumni_id", default="123456789")
@click.argument("job_categories", nargs=-1, type=str)
def add_categories_command(alumni_id, job_categories):
    #alumni = add_categories(alumni_id, job_categories)

    if alumni is None:
        print(f'Error adding categories')
    else:
        print(f'{alumni} categories added!')

# flask alumni apply
@alumni_cli.command("apply", help="Applies an alumni to a job listing")
@click.argument('alumni_id', default='123456789')
@click.argument('listing_title', default='listing1')
def apply_listing_command(alumni_id, listing_title):
    listing = get_listing_title(listing_title)
    
    alumni = apply_listing(alumni_id, listing.id)

    if alumni is None:
        print(f'Error applying to listing {listing_title}')
    else:
        print(f'{alumni} applied to listing {listing_title}')

#flask alumni set_modal_seen
@alumni_cli.command("set_modal_seen", help="Sets the 'has_seen_modal' field for an alumni")
@click.argument('alumni_id', default='123456789')
def set_modal_seen_command(alumni_id):
    try:
        print(f'Alumni {alumni_id} has seen the modal.')
    except Exception as e:
        print(f'Error setting modal seen for alumni {alumni_id}: {e}')

app.cli.add_command(alumni_cli)

# company commands
company_cli = AppGroup('company', help='Company object commands')

# flask company list
@company_cli.command("list", help="Lists company in the database")
@click.argument("format", default="string")
def list_company_command(format):
    if format == 'string':
        print(get_all_companies())
    else:
        print(get_all_companies_json())

# flask company add
@company_cli.command("add", help = "Add an copmany object to the database")
#@click.argument("username", default="representative name")
@click.argument("company_name", default="aah pull")
@click.argument("password", default="password")
@click.argument("email", default="aahpull@mail")
@click.argument("company_address", default="aahpull address")
@click.argument("contact", default="8689009000")
@click.argument("company_website", default="https://www.aahpull.com")
# @click.argument("job_categories", default='Database')
def add_company_command(company_name, password, email, mailing_address, public_email, phone_number, website_url):
    company = add_company(company_name, password, email, mailing_address, public_email, phone_number, website_url)

    if company is None:
        print('Error creating company')
    else:
        print(f'{company} created!')

#flask company notifications 
@company_cli.command("notifications", help="Show all notifications for a company")
@click.argument("company_name", default="company1")
def show_notifications(company_name):
    listings = get_company_listings(company_name)
    notifications = []
    
    for listing in listings:
        notifications.extend(listing.get_notifications())
    
    if notifications:
        for notification in notifications:
            print(f"Notification: {notification.message} (Timestamp: {notification.created_at})")
    else:
        print(f"No notifications found for {company_name}.")


app.cli.add_command(company_cli)

# listing commands
listing_cli = AppGroup('listing', help='Listing object commands')

# flask listing list
@listing_cli.command("list", help="Lists listings in the database")
@click.argument("format", default="string")
def list_listing_command(format):
    if format == 'string':
        print(get_all_listings())
    else:
        print(get_all_listings_json())

# flask listing add
# Note: you have to manually enter in the job categories here eg: flask listing add listingtitle desc company1 Database
@listing_cli.command("add", help="Add listing object to the database")
@click.argument("title", default="Job offer 1")
@click.argument("description", default="very good job :)")
@click.argument("company_name", default="company1")
@click.argument("salary", default="10000")
@click.argument("position", default="Full-time")
@click.argument("remote", default="True")
@click.argument("ttnational", default="True")
@click.argument("desiredcandidate", default="Technical Skills")
@click.argument("area", default="Laventille")
@click.argument("job_categories", nargs=-1, type=str)
def add_listing_command(title, description, company_name, salary, position, remote, ttnational, desiredcandidate, area, job_categories):
    listing = add_listing(title, description, company_name, salary, position, remote, ttnational, desiredcandidate, area, job_categories)

    if listing is None:
        print(f'Error adding categories')
    else:
        print(f'{listing} added!')

# flask listing delete
@listing_cli.command("delete", help="delete listing object from the database")
@click.argument("id", default="1")
def delete_listing_command(id):

    # listing = get_listing(id)

    deleted = delete_listing(id)

    if deleted is not None:
        print('Listing deleted')
    else:
        print('Listing not deleted')

# flask listing applicants
@listing_cli.command("applicants", help="Get all applicants for the listing")
@click.argument("listing_id", default='1')
def get_listing_applicants_command(listing_id):
    applicants = get_all_applicants(listing_id)

    if applicants is None:
        print(f'Error getting applicants')
    else:
        print(applicants)

app.cli.add_command(listing_cli)


'''
Test Commands
'''
test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
import click
from flask.cli import AppGroup
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers.alumnus_account import (
    add_alumnus_account,
    get_all_alumnus_accounts
)

alumnus_cli = AppGroup("alumns", help="AlumnusAccount object commands")

"""
===== CREATE =====
"""


@alumnus_cli.command("add", help="Creates and adds a new admin to the database.")
@click.argument("login_email")
@click.argument("password")
@click.argument("first_name")
@click.argument("last_name")
@click.option("--phone_number", default=None, help="Alumnus' phone number")
@click.option("--profile_photo_file_path", default=None, help="File path to profile photo")
def add_alumnus_account_command(
    login_email, password, first_name, last_name, phone_number, profile_photo_file_path
):
    """
    Command to create a new alumnus account.

    Args:
        login_email (str): The unique email used to log into the alumnus" account.
        password (str): The alumnus" password (hashed internally before storage).
        first_name (str): The alumnus" first name.
        last_name (str): The alumnus" last name.
        phone_number (str, optional): The alumnus" phone number.
        profile_photo_file_path (str, optional): The file path to the alumnus" profile photo.

    Returns:
        AlumnusAccount: The newly added alumnus account if successful.
    """
    alumnus_account = add_alumnus_account(
        login_email, password, first_name, last_name, phone_number, profile_photo_file_path
    )
    click.echo(
        f"Alumnus account created: {alumnus_account.first_name} {alumnus_account.last_name}")


"""
===== READ =====
"""
"""
===== UPDATE =====
"""
"""
===== DELETE =====
"""


@alumnus_cli.command("list", help="Lists alumnis in the database")
@click.option("--jsonify-results", is_flag=True, help="Return results in JSON format")
def list_listing_command(jsonify_results):
    print(get_all_alumnus_accounts(jsonify_results))


@alumnus_cli.command("add", help="Add an alumni object to the database")
@click.argument("login_email", default="rob@mail2")
@click.argument("password_hash", default="robpass")
@click.argument("firstname", default="rob2fname")
@click.argument("lastname", default="rob2lname")
@click.argument("phone_number", default="(555)-555-5555")
def add_alumni_command(password, login_email, phone_number, firstname, lastname):
    alumni = add_alumnus_account(
        login_email,
        password,
        firstname,
        lastname,
        phone_number=phone_number
    )

    if alumni is None:
        print("Error creating alumni")
    else:
        print(f"{alumni} created!")

# flask alumni subscribe
# add in better error checking for subscribe_action - try except that the user exists


# @alumnus_cli.command("subscribe", help="Subscribe an alumni object")
# @click.argument("alumni_id", default="123456789")
# def subscribe_alumni_command(alumni_id):
#     alumni = subscribe(alumni_id)

#     if alumni is None:
#         print("Error subscribing alumni")
#     else:
#         if is_alumni_subscribed(alumni_id):
#             print(f"{alumni} subscribed!")
#         else:
#             print(f"{alumni} unsubscribed!")

# flask alumni add_categories
# note, must manually add in job_categories in the cli command eg: flask alumni add_categories 123456789 Database,Programming
# @alumnus_cli.command("add_categories", help="Add job categories for the user")
# @click.argument("job_categories", nargs=-1, type=str)
# def add_categories_command(alumni_id, job_categories):
#     alumni = add_categories(alumni_id, job_categories)

#     if alumni is None:
#         print(f"Error adding categories")
#     else:
#         print(f"{alumni} categories added!")

# flask alumni apply


# @alumnus_cli.command("apply", help="Applies an alumni to a job listing")
# @click.argument("listing_id", default="1")
# def apply_listing_command(listing_title):
#     listing = get_listing_title(listing_title)

#     alumni = apply_listing(listing.id)

#     if alumni is None or job_listing is None:
#         print(f"Error applying to job listing listing {listing_id}")
#     else:
#         print(f"{alumni} applied to listing {listing_title}")

# flask alumni set_modal_seen

# have to fix
# @alumnus_cli.command("set_modal_seen", help="Sets the "has_seen_modal" field for an alumni")
# @click.argument("alumni_id", default="123456789")
# def set_modal_seen_command(alumni_id):
#     try:
#         set_alumni_modal_seen(alumni_id)
#         print(f"Alumni {alumni_id} has seen the modal.")
#     except Exception as e:
#         print(f"Error setting modal seen for alumni {alumni_id}: {e}")

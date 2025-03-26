import click
from flask.cli import AppGroup
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from App.controllers.admin_account import (
    add_admin_account,
    get_admin_account,
    get_admin_account_by_login_email,
    get_all_admin_accounts,
    update_admin_account_login_email,
    update_admin_account_password,
    update_admin_account_profile_photo,
    delete_admin_account,
)

admin_cli = AppGroup('admin', help='AdminAccount object commands')

"""
===== CREATE =====
"""


@admin_cli.command("add", help="Creates and adds a new admin to the database.")
@click.argument("login_email")
@click.argument("password")
@click.option(
    "--profile-photo",
    "profile_photo_file_path",
    default=None,
    help="Path to the profile photo (optional)."
)
def add_admin_account_command(login_email, password, profile_photo_file_path):
    """
    Adds a new admin account to the database.

    Args:
        login_email (str): The email address for the new admin.
        password (str): The password for the new admin.
        profile_photo_file_path (str, optional): Path to the profile photo file. Defaults to None.

    Raises:
        ValueError: If login_email or password is empty.
    """
    try:
        if not login_email or not password:
            raise ValueError("Login email and password are required.")

        add_admin_account(
            login_email,
            password,
            profile_photo_file_path
        )
        click.echo(f"Admin {login_email} added successfully.")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)


"""
===== READ =====
"""


@admin_cli.command("get", help="Retrieves an admin account by ID.")
@click.argument("admin_id", type=int)
def get_admin_command(admin_id):
    """
    Fetches an admin account using the given ID.

    Args:
        admin_id (int): The admin's unique ID.
    """
    admin = get_admin_account(admin_id)
    if admin:
        click.echo(f"Admin ID: {admin.id}, Email: {admin.login_email}")
    else:
        click.echo(f"Admin with ID {admin_id} not found.", err=True)


@admin_cli.command("get-by-email", help="Retrieves an admin account by login email.")
@click.argument("login_email")
def get_admin_by_email_command(ctx, login_email):
    """
    Retrieves an admin account based on the given login email.

    Args:
        login_email (str): The login email of the admin account to fetch.
    """
    admin = get_admin_account_by_login_email(login_email)
    if admin:
        click.echo(f"Admin ID: {admin.id}, Email: {admin.login_email}")
    else:
        click.echo(f"Admin with email {login_email} not found.", err=True)


@admin_cli.command("list", help="Lists all admin accounts.")
@click.option(
    "--json",
    "jsonify_results",
    is_flag=True,
    help="Output results in JSON format."
)
def list_admins_command(jsonify_results):
    """
    Lists all admin accounts in the database.

    Args:
        jsonify_results (bool): Whether to output results in JSON format.
    """
    admins = get_all_admin_accounts(jsonify_results)
    if admins:
        for admin in admins:
            click.echo(
                admin if jsonify_results else f"ID: {admin.id}, Email: {admin.login_email}"
            )
    else:
        click.echo("No admin accounts found.")


"""
===== UPDATE =====
"""


@admin_cli.command("update-email", help="Updates an admin's login email.")
@click.argument("admin_id", type=int)
@click.argument("password")
@click.argument("new_login_email")
def update_admin_email_command(admin_id, password, new_login_email):
    """
    Updates an admin's email after verifying the current password.

    Args:
        admin_id (int): The admin's ID.
        password (str): The current password for authentication.
        new_login_email (str): The new email to update.
    """
    try:
        updated_admin = update_admin_account_login_email(
            admin_id,
            password,
            new_login_email
        )
        click.echo(
            f"Admin ID {admin_id} updated email to {updated_admin.login_email}.")
    except (ValueError, PermissionError, IntegrityError, SQLAlchemyError) as e:
        click.echo(f"Error: {e}", err=True)


@admin_cli.command("update-password", help="Updates an admin's password.")
@click.argument("admin_id", type=int)
@click.argument("current_password")
@click.argument("new_password")
def update_admin_password_command(admin_id, current_password, new_password):
    """
    Updates an admin's password after verifying the current password.

    Args:
        admin_id (int): The admin's ID.
        current_password (str): The current password.
        new_password (str): The new password to set.
    """
    try:
        update_admin_account_password(
            admin_id,
            current_password,
            new_password
        )
        click.echo(f"Admin ID {admin_id} password updated successfully.")
    except (ValueError, PermissionError, SQLAlchemyError) as e:
        click.echo(f"Error: {e}", err=True)


@admin_cli.command("update-profile-photo", help="Updates an admin's profile photo.")
@click.argument("admin_id", type=int)
@click.argument("new_profile_photo_file_path")
def update_admin_profile_photo_command(ctx, admin_id, new_profile_photo_file_path):
    """
    Updates the profile photo of an admin account.

    Args:
        admin_id (int): The admin's ID whose profile photo is to be updated.
        new_profile_photo_file_path (str): The new profile photo file path.
    """
    try:
        updated_admin = update_admin_account_profile_photo(
            admin_id, new_profile_photo_file_path)
        click.echo(
            f"Admin ID {admin_id}'s profile photo updated successfully.")
    except (ValueError, SQLAlchemyError) as e:
        click.echo(f"Error: {e}", err=True)


"""
===== DELETE =====
"""


@admin_cli.command("delete", help="Deletes an admin account (requires JWT authentication).")
@click.argument("target_id", type=int)
@jwt_required()
@click.pass_context
def delete_admin_command(ctx, target_id):
    """
    Deletes an admin account only if the requester is authenticated via JWT.

    Args:
        target_id (int): The ID of the admin to be deleted.

    Raises:
        ValueError: If the requester is not logged in or tries to delete themselves.
        PermissionError: If the requester lacks admin privileges.
    """

    # Get the logged-in admin's ID from the JWT token
    requester_id = get_jwt_identity()

    # Ensure the requester exists and is an admin
    requester = get_admin_account(requester_id)
    if not requester:
        click.echo(
            "Error: You must be a logged-in admin to perform this action.", err=True)
        return

    # Prevent self-deletion
    if target_id == requester_id:
        click.echo("Error: You cannot delete yourself.", err=True)
        return

    try:
        # Proceed with deletion
        delete_admin_account(target_id, requester_id)
        click.echo(f"Admin ID {target_id} deleted successfully.")

    except (ValueError, PermissionError, SQLAlchemyError) as e:
        click.echo(f"Error: {e}", err=True)


# have to fix
# @admin_cli.command("toggle", help="Approve or disapprove a job listing")
# @click.argument("listing_id", default='1')
# def toggle_approval_command(listing_id):
#     result = toggle_listing_approval(listing_id)

#     if result is None:
#         print(
#             f"Listing with ID {listing_id} not found or could not be approved.")
#     else:
#         print(
#             f"Listing with ID {listing_id} has been {'approved' if result else 'disapproved'}.")

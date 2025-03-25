from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional, Union

from App.database import db
from App.models import BaseUserAccount, AdminAccount
from App.utils.db_utils import get_records_by_filter, validate_email

"""
------ CREATE ------
"""


def add_admin(login_email: str, password: str, profile_photo_file_path: str = None):
    """
    Adds a new admin account to the database.

    Args:
        login_email (str): The unique email used to log into the admin's account.
        password (str): The admin's plaintext password (hashed internally before storage).
        profile_photo_file_path (Optional[str]): The file path to the admin's profile photo.

    Returns:
        AdminAccount: The newly added admin if successful.

    Raises:
        IntegrityError: If a database constraint is violated (e.g., duplicate email).
    """

    # Check if email exists in any subclass of BaseUserAccount dynamically
    for subclass in BaseUserAccount.__subclasses__():
        if subclass.query.filter_by(login_email=login_email).first():
            return None  # Email already exists

    new_admin = AdminAccount(
        login_email=login_email,
        password=password,
        profile_photo_file_path=profile_photo_file_path
    )

    try:
        db.session.add(new_admin)
        db.session.commit()
        return new_admin

    except IntegrityError as e:
        print(e)
        db.session.rollback()
        return None

    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return None


"""
------ READ/GET (SINGLE RECORD) ------
"""


def get_admin_account(id: int) -> Optional[AdminAccount]:
    """
    Retrieves a admin account by its unique identifier.

    Args:
        id (int): The unique ID of the admin account.

    Returns:
        Optional[AdminAccount]: The matching admin account if found, otherwise None.
    """
    return AdminAccount.query.filter_by(id=id).first()


def get_admin_account_by_login_email(login_email: str) -> Optional[AdminAccount]:
    """
    Retrieves a admin account by its unique login email.

    Args:
        id (int): The unique login_email of the admin account.

    Returns:
        Optional[AdminAccount]: The matching admin account if found, otherwise None.
    """
    return AdminAccount.query.filter_by(login_email=login_email).first()


"""
------ READ/GET (MULTIPLE RECORDS) ------
"""


def get_all_admin_accounts(jsonify_results: bool = False) -> Union[List[AdminAccount], List[dict]]:
    """
    Retrieves all admin accounts from the database.

    Args:
        jsonify_results (bool, optional): If True, returns admin accounts as a list of JSON-serializable dictionaries.
                                          Defaults to False.

    Returns:
        Union[List[AdminAccount], List[dict]]: 
            - If `jsonify_results` is False, returns a list of `AdminAccount` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no admin accounts are found.
    """
    return get_records_by_filter(
        AdminAccount,
        lambda: AdminAccount.query.all(),
        jsonify_results
    )


def get_admin_accounts_by_profile_photo_file_path(profile_photo_file_path: str, jsonify_results: bool = False) -> Union[List[AdminAccount], List[dict]]:
    """
    Retrieves all admin accounts with the given profile photo file path.

    Args:
        profile_photo_file_path (str): The file path to the admin's profile photo
        jsonify_results (bool, optional): If True, returns admin accounts as a list of JSON-serializable dictionaries.
                                          Defaults to False.

    Returns:
        Union[List[AdminAccount], List[dict]]: 
            - If `jsonify_results` is False, returns a list of `AdminAccount` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no admin accounts are found.
    """
    return get_records_by_filter(
        AdminAccount,
        lambda: AdminAccount.query.filter_by(
            profile_photo_file_path=profile_photo_file_path
        ),
        jsonify_results
    )


"""
------ UPDATE ------
"""


def update_admin_login_email(id: int, password: str, int, new_email: str) -> bool:
    """
    Updates the login email of an admin account after verifying their password.

    Args:
        id (int): The ID of the admin whose email is being updated.
        password (str): The current password to verify identity.
        new_email (str): The new email address to update.

    Returns:
        AdminAccount: The updated AdminAccount if successful.

    Raises:
        ValueError: If the admin id, new email, or password are empty or invalid.
        PermissionError: If the password is incorrect.
        IntegrityError: If the new email is already taken.
        SQLAlchemyError: For any other database-related issues.
    """
    admin = get_admin_account(id)
    if not admin:
        raise ValueError(f"Admin with id <{id}> not found.")

    if not password:
        raise ValueError("Invalid password <[HIDDEN]>.")

    if not admin.check_password(password):
        raise PermissionError("Incorrect password <[HIDDEN]>.")

    if not (new_email and validate_email(new_email)):
        raise ValueError(f"Invalid email <'{new_email}'>.")

    try:
        admin.login_email = new_email
        db.session.commit()
        print("Login email updated successfully.")
        return admin

    except IntegrityError:
        db.session.rollback()
        raise IntegrityError("Error: Email address already in use.")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


def update_admin_password(id: int, password: str, new_password: str) -> bool:
    """
    Updates the password of an admin account after verifying their existing password.

    Args:
        id (int): The ID of the admin whose email is being updated.
        password (str): The current password to verify identity.
        new_password (str): The new password to update.

    Returns:
        AdminAccount: The updated AdminAccount if successful.

    Raises:
        ValueError: If the admin id, new email, or password are empty or invalid.
        PermissionError: If the password is incorrect.
        IntegrityError: If the new email is already taken.
        SQLAlchemyError: For any other database-related issues.
    """
    admin = get_admin_account(id)
    if not admin:
        raise ValueError(f"Admin with id <{id}> not found.")

    if not password:
        raise ValueError("Invalid password <[HIDDEN]>.")

    if not admin.check_password(password):
        raise PermissionError("Incorrect password <[HIDDEN]>.")

    if not (new_password):
        raise ValueError(f"Invalid new password <'{new_password}'>.")

    try:
        admin.set_password(new_password)
        db.session.commit()
        print("Password updated successfully.")
        return admin

    except IntegrityError:
        db.session.rollback()
        raise IntegrityError("Error: Email address already in use.")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


def update_admin_profile_photo(id: int, new_profile_photo_file_path: str) -> bool:
    """
    Updates the profile photo of an admin account.

    Args:
        id (int): The ID of the admin whose email is being updated.
        new_profile_photo_file_path (str): The new profile photo's file path to update.

    Returns:
        AdminAccount: The updated AdminAccount if successful.

    Raises:
        ValueError: If the admin id is invalid.
        SQLAlchemyError: For any database-related issues.
    """
    admin = get_admin_account(id)
    if not admin:
        raise ValueError(f"Admin with id <{id}> not found.")

    try:
        admin.profile_photo_file_path = new_profile_photo_file_path
        db.session.commit()
        print("Profile photo updated successfully.")
        return admin

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


"""
------ DELETE
"""


def delete_admin_account(target_id: int, requester_id: int) -> None:
    """
    Securely deletes an admin account if the requester is also an admin.

    Args:
        target_id (int): The ID of the admin account to delete.
        requester_id (int): The ID of the admin requesting the deletion.

    Raises:
        ValueError: If the targeted account does not exist, or the requester tries to delete themselves.
        PermissionError: If the requester is not an admin/does not exist.
        SQLAlchemyError: For any database-related issues.
    """
    if target_id == requester_id:
        raise ValueError(
            "Cannot request self-deletion. There must always be at least one admin.")

    admin_to_delete = get_admin_account(target_id)
    if not admin_to_delete:
        raise ValueError(
            f"Target admin account with id <{target_id}> not found")

    requesting_admin = get_admin_account(requester_id)
    if not requesting_admin:
        raise PermissionError(
            f"Requester admin account with id <{requester_id}> not found")

    try:
        db.session.delete(admin_to_delete)
        db.session.commit()
        print(f"Admin account with id <'{id}'> deleted successfully")

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deleting admin account with id <'{id}'>: {e}")


# def delete_listing(jobListing_id):
#     from .job_listing import get_listing

#     joblisting = get_listing(jobListing_id)

#     if joblisting is not None:
#         db.session.delete(joblisting)
#         db.session.commit()
#         return True

#     return None

# # delete other listings


# def delete_listing(listing_id):
#     from .job_listing import get_listing

#     listing = get_listing(listing_id)

#     if listing is not None:
#         db.session.delete(listing)
#         db.session.commit()
#         return True

#     return None


# def toggle_listing_approval(listing_id, status):
#     print("toggle listing approval function")
#     from .job_listing import get_listing

#     listing = get_listing(listing_id)
#     if not listing:
#         return None
#     if status in ["APPROVED", "PENDING", "REJECTED"]:
#         listing.admin_approval_status = status
#     else:
#         return None

#     try:
#         db.session.commit()
#         return True
#     except Exception as e:
#         print(f'my error: {e}')
#         db.session.rollback()
#         return None

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional, Union

from App.database import db
from App.models import BaseUserAccount, AdminAccount
from App.utils.db_utils import get_records_by_filter, validate_email

"""
===== CREATE =====
"""


def add_admin_account(login_email: str, password: str, profile_photo_file_path: str = None) -> AdminAccount:
    """
    Adds a new admin account to the database.

    Args:
        login_email (str): The unique email used to log into the admin's account.
        password (str): The admin's plaintext password (hashed internally before storage).
        profile_photo_file_path (Optional[str]): The file path to the admin's profile photo.

    Returns:
        AdminAccount: The newly added admin account if successful.

    Raises:
        ValueError: If the provided login email already exists for an account.
        IntegrityError: If a database constraint is violated.
        SQLAlchemyError: For other database-related issues.
    """

    # Check if unique fields exist in any subclass of BaseUserAccount dynamically
    for subclass in BaseUserAccount.__subclasses__():
        if subclass.query.filter_by(login_email=login_email).first():
            raise ValueError(
                f"Login email '{login_email}' already exists for another account."
            )

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
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


"""
===== READ/GET (SINGLE RECORD) =====
"""


def get_admin_account(id: int) -> Optional[AdminAccount]:
    """
    Retrieves a admin account by its unique identifier.

    Args:
        id (int): The unique ID of the admin account.

    Returns:
        Optional[AdminAccount]: The matching admin account if found, otherwise None.
    """
    return db.session.get(AdminAccount, id)


def get_admin_account_by_login_email(login_email: str) -> Optional[AdminAccount]:
    """
    Retrieves a admin account by its unique login email.

    Args:
        id (int): The unique login_email of the admin account.

    Returns:
        Optional[AdminAccount]: The matching admin account if found, otherwise None.
    """
    return AdminAccount.query.filter_by(login_email=login_email)


"""
===== READ/GET (MULTIPLE RECORDS) =====
"""


def get_all_admin_accounts(jsonify_results: bool = False) -> Union[List[AdminAccount], List[dict]]:
    """
    Retrieves all admin accounts from the database.

    Args:
        jsonify_results (bool, optional):
            If True, returns admin accounts as a list of JSON-serializable dictionaries.
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


def get_admin_accounts_by_profile_photo_file_path(
        profile_photo_file_path: str, jsonify_results: bool = False
) -> Union[List[AdminAccount], List[dict]]:
    """
    Retrieves all admin accounts with the given profile photo file path.

    Args:
        profile_photo_file_path (str): The file path to the admin's profile photo
        jsonify_results (bool, optional):
            If True, returns admin accounts as a list of JSON-serializable dictionaries.
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
===== UPDATE =====
"""


def update_admin_account_login_email(
        id: int, password: str, new_login_email: str
) -> AdminAccount:
    """
    Securely updates the alumnus' login email after verifying their current password.

    Args:
        id (int): The admin's ID.
        password (str): The admin's current password for authentication.
        new_email (str): The new login email.

    Returns:
        AdminAccount: The updated admin account.

    Raises:
        ValueError: If the input is invalid or the admin was not found.
        PermissionError: If the current password is incorrect.
        IntegrityError: If the new login email is already in use.
        SQLAlchemyError: For other database-related issues.
    """
    admin = get_admin_account(id)
    if not admin:
        raise ValueError(f"Admin with id {id} was not found.")

    if not password or not admin.check_password(password):
        raise PermissionError("Incorrect password.")

    if not (new_login_email and validate_email(new_login_email)):
        raise ValueError(f"Invalid email '{new_login_email}'.")

    try:
        admin.login_email = new_login_email
        db.session.commit()
        return admin

    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_admin_account_password(
        id: int, current_password: str, new_password: str
) -> AdminAccount:
    """
    Securely updates the admin' password after verifying their current password.

    Args:
        id (int): The admin's ID.
        current_password (str): The admin's current password for authentication.
        new_password (str): The new password.

    Returns:
        AdminAccount: The updated admin account.

    Raises:
        ValueError: If the input is invalid or the admin was not found.
        PermissionError: If the current password is incorrect.
        SQLAlchemyError: For other database-related issues.
    """
    admin = get_admin_account(id)
    if not admin:
        raise ValueError(f"Admin with id {id} was not found.")

    if not current_password or not admin.check_password(current_password):
        raise PermissionError("Incorrect password.")

    if not (new_password):
        raise ValueError("New password cannot be empty.")

    try:
        admin.set_password(new_password)
        db.session.commit()
        return admin

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_admin_account_profile_photo(id: int, new_profile_photo_file_path: str) -> AdminAccount:
    """
    Updates the profile photo of an admin account.

    Args:
        id (int): The admin's ID.
        new_profile_photo_file_path (str): The new profile photo's file path.

    Returns:
        AdminAccount: The updated admin account if successful.

    Raises:
        ValueError: If the input is invalid or the admin was not found.
        SQLAlchemyError: For any database-related issues.
    """
    admin = get_admin_account(id)
    if not admin:
        raise ValueError(f"Admin with id {id} was not found.")

    try:
        admin.profile_photo_file_path = new_profile_photo_file_path
        db.session.commit()
        return admin

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


"""
===== DELETE =====
"""


def delete_admin_account(target_id: int, requester_id: int) -> None:
    """
    Securely deletes an admin account if the requester is also an admin.

    Args:
        target_id (int): The ID of the admin account to be deleted.
        requester_id (int): The ID of the admin requesting the deletion.

    Raises:
        ValueError: If the targeted account does not exist, or the requester tries to delete themselves.
        PermissionError: If the requester does not exist or lacks permissions.
        SQLAlchemyError: For other database-related issues.
    """
    if target_id == requester_id:
        raise ValueError(
            "Cannot request self-deletion. There must always be at least one admin."
        )

    admin_to_delete = get_admin_account(target_id)
    if not admin_to_delete:
        raise ValueError(
            f"Target admin account with id {target_id} was not found.")

    if not get_admin_account(requester_id):
        raise PermissionError(
            f"Requester (Admin ID {requester_id}) was not found or lacks permissions."
        )

    try:
        db.session.delete(admin_to_delete)
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occured: {e}")

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

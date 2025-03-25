from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional, Union

from App.database import db
from App.models import BaseUserAccount, AdminAccount, AlumnusAccount
from App.utils.db_utils import get_records_by_filter, validate_email

"""
===== CREATE =====
"""


def add_alumnus_account(
        login_email: str, password: str, first_name: str, last_name: str,
        phone_number: str = None, profile_photo_file_path: str = None
) -> AlumnusAccount:
    """
    Adds a new alumnus account to the database.

    Args:
        login_email (str): The unique email used to log into the alumnus' account.
        password (str): The alumnus' plaintext password (hashed internally before storage).
        first_name (str): The alumnus' first name.
        last_name (str): The alumnus' last name.
        phone_number (str, optional): The alumnus' unique phone number, which may include country codes and extensions.
        profile_photo_file_path (str, optional): The file path to the alumnus' profile photo.

    Returns:
        AlumnusAccount: The newly added alumnus account if successful.

    Raises:
        ValueError: If the provided login email already exists for an account.
        IntegrityError: If a database constraint is violated.
        SQLAlchemyError: For other database-related issues.
    """

    # Check for existing accounts with duplicate fields
    check_fields = {
        "login_email": login_email, "phone_number": phone_number
    }

    for field, value in check_fields.items():
        if value:
            for subclass in BaseUserAccount.__subclasses__():
                if subclass.query.filter_by(**{field: value}).first():
                    raise ValueError(
                        f"{field.replace('_', ' ').title()} <'{value}'> already exists."
                    )

    new_alumnus = AlumnusAccount(
        login_email=login_email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        profile_photo_file_path=profile_photo_file_path
    )

    try:
        db.session.add(new_alumnus)
        db.session.commit()
        return new_alumnus

    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


"""
===== READ/GET (SINGLE RECORD) =====
"""


def get_alumnus_account(id: int) -> Optional[AlumnusAccount]:
    """
    Retrieves an alumnus account by its unique identifier.

    Args:
        id (int): The alumnus' ID.

    Returns:
        Optional[AlumnusAccount]: The matching alumnus account if found, otherwise None.
    """
    return db.session.get(AlumnusAccount, id)


def get_alumnus_account_by_login_email(login_email: str) -> Optional[AlumnusAccount]:
    """
    Retrieves an alumnus account by its unique login email.

    Args:
        id (int): The alumnus' login email.

    Returns:
        Optional[AlumnusAccount]: The matching alumnus account if found, otherwise None.
    """
    return AlumnusAccount.query.filter_by(login_email=login_email).first()


def get_alumnus_accounts_by_phone_number(phone_number: str) -> Optional[AlumnusAccount]:
    """
    Retrieves an alumnus accounts by its unique phone number.

    Args:
        phone number (str): The alumnus' phone number.

    Returns:
        Optional[AlumnusAccount]: The matching alumnus account if found, otherwise None.
    """
    return AlumnusAccount.query.filter_by(phone_number=phone_number).first()


"""
===== READ/GET (MULTIPLE RECORDS) =====
"""


def get_all_alumnus_accounts(
        jsonify_results: bool = False
) -> Union[List[AlumnusAccount], List[dict]]:
    """
    Retrieves all alumnus accounts from the database.

    Args:
        jsonify_results (bool, optional):
            If True, returns alumnus accounts as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[AlumnusAccount], List[dict]]: 
            - If `jsonify_results` is False, returns a list of `AlumnusAccount` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no alumnus accounts are found.
    """
    return get_records_by_filter(
        AlumnusAccount,
        lambda: AlumnusAccount.query.all(),
        jsonify_results
    )


def get_alumnus_accounts_by_first_name(
        first_name: str, jsonify_results: bool = False
) -> Union[List[AlumnusAccount], List[dict]]:
    """
    Retrieves all alumnus accounts with the given first name.

    Args:
        first_name (str): The alumnus' first name
        jsonify_results (bool, optional):
            If True, returns alumnus accounts as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[AlumnusAccount], List[dict]]: 
            - If `jsonify_results` is False, returns a list of `AlumnusAccount` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no alumnus accounts are found.
    """
    return get_records_by_filter(
        AlumnusAccount,
        lambda: AlumnusAccount.query.filter_by(
            first_name=first_name
        ),
        jsonify_results
    )


def get_alumnus_accounts_by_last_name(
        last_name: str, jsonify_results: bool = False
) -> Union[List[AlumnusAccount], List[dict]]:
    """
    Retrieves all alumnus accounts with the given last name.

    Args:
        first_name (str): The alumnus' last name
        jsonify_results (bool, optional):
            If True, returns alumnus accounts as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[AlumnusAccount], List[dict]]: 
            - If `jsonify_results` is False, returns a list of `AlumnusAccount` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no alumnus accounts are found.
    """
    return get_records_by_filter(
        AlumnusAccount,
        lambda: AlumnusAccount.query.filter_by(
            last_name=last_name
        ),
        jsonify_results
    )


def get_alumnus_accounts_by_profile_photo_file_path(
        profile_photo_file_path: str, jsonify_results: bool = False
) -> Union[List[AlumnusAccount], List[dict]]:
    """
    Retrieves all alumnus accounts with the given profile photo file path.

    Args:
        profile_photo_file_path (str): The file path to the alumnus's profile photo
        jsonify_results (bool, optional):
            If True, returns alumnus accounts as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[AlumnusAccount], List[dict]]: 
            - If `jsonify_results` is False, returns a list of `AlumnusAccount` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no alumnus accounts are found.
    """
    return get_records_by_filter(
        AlumnusAccount,
        lambda: AlumnusAccount.query.filter_by(
            profile_photo_file_path=profile_photo_file_path
        ),
        jsonify_results
    )


"""
===== UPDATE =====
"""


def update_alumnus_account_login_email(
        id: int, password: str, new_login_email: str
) -> AlumnusAccount:
    """
    Securely updates the alumnus' login email after verifying their current password.

    Args:
        id (int): The alumnus' ID.
        password (str): The alumnus' current password for authentication.
        new_login_email (str): The new login email.

    Returns:
        AlumnusAccount: The updated alumnus account if successful.

    Raises:
        ValueError: If input is invalid or the alumnus was not found.
        PermissionError: If the current password is incorrect.
        IntegrityError: If the new email is already taken.
        SQLAlchemyError: For other database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id {id} not found.")

    if not password or not alumnus.check_password(password):
        raise PermissionError("Incorrect password.")

    if not (new_login_email and validate_email(new_login_email)):
        raise ValueError(f"Invalid login email '{new_login_email}'.")

    try:
        alumnus.login_email = new_login_email
        db.session.commit()
        return alumnus

    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_alumnus_account_password(id: int, password: str, new_password: str) -> AlumnusAccount:
    """
    Securely updates the alumnus' password after verifying their current password.

    Args:
        id (int): The alumnus' ID.
        password (str): The alumnus' current password for authentication.
        new_password (str): The new password.

    Returns:
        AlumnusAccount: The updated alumnus account if successful.

    Raises:
        ValueError: If input is invalid or the alumnus was not found.
        PermissionError: If the current password is incorrect.
        SQLAlchemyError: For other database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id {id} not found.")

    if not password or not alumnus.check_password(password):
        raise PermissionError("Incorrect password.")

    if not (new_password):
        raise ValueError("New password cannot be empty.")

    try:
        alumnus.set_password(new_password)
        db.session.commit()
        return alumnus

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_alumnus_account_first_name(id: int, new_first_name: str) -> AlumnusAccount:
    """
    Updates the alumnus' first name.

    Args:
        id (int): The alumnus' ID.
        new_first_name (str): The new first name.

    Returns:
        AlumnusAccount: The updated alumnus account if successful.

    Raises:
        ValueError: If the alumnus was not found.
        SQLAlchemyError: For any database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id {id} not found.")

    try:
        alumnus.first_name = new_first_name
        db.session.commit()
        return alumnus

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_alumnus_account_last_name(id: int, new_last_name: str) -> AlumnusAccount:
    """
    Updates the alumnus' last name.

    Args:
        id (int): The alumnus' ID.
        new_last_name (str): The new last name.

    Returns:
        AlumnusAccount: The updated alumnus account if successful.

    Raises:
        ValueError: If the alumnus id is invalid.
        SQLAlchemyError: For any database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id {id} not found.")

    try:
        alumnus.last_name = new_last_name
        db.session.commit()
        print("Last name updated successfully.")
        return alumnus

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_alumnus_account_phone_number(id: int, new_phone_number: str) -> AlumnusAccount:
    """
    Updates the alumnus' unique phone number.

    Args:
        id (int): The ID of the alumnus whose email is being updated.
        new_phone_number (str): The new, unique phone number to update.

    Returns:
        AlumnusAccount: The updated alumnus account if successful.

    Raises:
        ValueError: If the alumnus id is invalid.
        IntegrityError: If the phone number is already in use.
        SQLAlchemyError: For any database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id {id} not found.")

    try:
        alumnus.phone_number = new_phone_number
        db.session.commit()
        print("Phone number updated successfully.")
        return alumnus

    except IntegrityError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database constraint violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_alumnus_account_profile_photo(
        id: int, new_profile_photo_file_path: str
) -> AlumnusAccount:
    """
    Updates the alumnus' profile photo.

    Args:
        id (int): The ID of the alumnus whose email is being updated.
        new_profile_photo_file_path (str): The new profile photo's file path to update.

    Returns:
        AlumnusAccount: The updated alumnus account if successful.

    Raises:
        ValueError: If the alumnus id is invalid.
        SQLAlchemyError: For any database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id {id} not found.")

    try:
        alumnus.profile_photo_file_path = new_profile_photo_file_path
        db.session.commit()
        print("Profile photo updated successfully.")
        return alumnus

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


"""
===== DELETE =====
"""


def delete_alumnus_account(target_id: int, requester_id: int) -> None:
    """
    Securely deletes an alumnus account if the requester is an admin.

    Args:
        target_id (int): The ID of the alumnus account to be deleted.
        requester_id (int): The ID of the admin requesting the deletion.

    Raises:
        ValueError: If the targeted account does not exist.
        PermissionError: If the requester does not exist or lacks permissions.
        SQLAlchemyError: For any database-related issues.
    """

    alumnus_to_delete = get_alumnus_account(target_id)
    if not alumnus_to_delete:
        raise ValueError(
            f"Target alumnus account with id {target_id} not found")

    if not db.session.get(AdminAccount, requester_id):
        raise PermissionError(
            f"Requester (Admin ID {requester_id}) not found or lacks permissions."
        )

    try:
        db.session.delete(alumnus_to_delete)
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
#         listing.alumnus_approval_status = status
#     else:
#         return None

#     try:
#         db.session.commit()
#         return True
#     except Exception as e:
#         print(f'my error: {e}')
#         db.session.rollback()
#         return None


# def is_alumni_subscribed(id):
#     # alumni = get_alumni(id)
#     # if(alumni.subscribed == True):
#     #     return True
#     # else:
#     return False


# # also needs to be rewritten entirely -CTZ
# def get_all_subscribed_alumni():
#     return get_all_alumni()
#     # all_alumni = AlumnusAccount.query.filter_by(subscribed=True).all()
#     # return all_alumni


# # Also needs to be re written -CTZ
# # handle subscribing and unsubscribing, this needs to be changed to handle subscribing to companies
# def subscribe(id, job_category=None):
#     alumni = get_alumni(id)

#     # if alumni is None:
#     #     print('nah')
    #     return None

    # alumni.subscribed = True

    # if job_category is not None:
    #     # add_categories(alumni_id, job_category)
    #     alumni.add_category(job_category)

    # db.session.add(alumni)
    # db.session.commit()
    # return alumni

# rewrite me -CTZ


# def unsubscribe(id):
#     alumni = get_alumni(id)

#     # if not alumni:
#     #     # print('nah')
#     #     return None

#     # alumni.subscribed = False
#     # remove_categories(id, alumni.get_categories())

#     # db.session.add(alumni)
#     # db.session.commit()
#     return alumni

# def subscribe_action(alumni_id, job_category=None):
#     alumni = get_alumni(alumni_id)

#     if not alumni:
#         # print('nah')
#         return None

#     # if they are already susbcribed then unsubscribe them
#     if is_alumni_subscribed(alumni_id):
#         alumni.subscribed = False
#         remove_categories(alumni_id, alumni.get_categories())

#     else:
#         alumni.subscribed = True

#         if job_category is not None:
#             add_categories(alumni_id, job_category)
#         # set their jobs list to job_category ?

#     db.session.add(alumni)
#     db.session.commit()
#     return alumni

# adding and removing job categories


# def set_alumni_modal_seen(id):
#     alumni = get_alumni(id)
#     alumni.has_seen_modal = True
#     db.session.commit()

# # To be re written - CTZ


# def get_approved_listings():
#     all_listings = JobListing.query.all()
#     my_approved_listings = []
#     for listing in all_listings:
#         if listing.alumnus_approval_status == "APPROVED":
#             my_approved_listings.append(listing)
#     return my_approved_listings

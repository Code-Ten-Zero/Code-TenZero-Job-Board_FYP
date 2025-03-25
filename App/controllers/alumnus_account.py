from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional, Union

from App.database import db
from App.models import BaseUserAccount, AdminAccount, AlumnusAccount
from App.utils.db_utils import get_records_by_filter, validate_email

"""
------ CREATE ------
"""


def add_alumnus(
        login_email: str, password: str, first_name: str, last_name: str,
        phone_number: str = None, profile_photo_file_path: str = None
):
    """
    Adds a new alumnus account to the database.

    Args:
        login_email (str): The unique email used to log into the alumnus' account.
        password (str): The alumnus' plaintext password (hashed internally before storage).
        first_name (str): The alumnus' first name.
        last_name (str): The alumnus' last name.
        phone_number (str, optional): The alumnus' unique phone number. Example: "+1-(868)-123-4567 ext. 8910"
        profile_photo_file_path (str, optional): The file path to the alumnus' profile photo.

    Returns:
        AlumnusAccount: The newly added alumnus if successful.

    Raises:
        IntegrityError: If a database constraint is violated (e.g., duplicate login email).
        SQLAlchemyError: For any other database-related issues.
    """

    # Check if email exists in any subclass of BaseUserAccount dynamically
    for subclass in BaseUserAccount.__subclasses__():
        if subclass.query.filter_by(login_email=login_email).first():
            return None  # Email already exists

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


def get_alumnus_account(id: int) -> Optional[AlumnusAccount]:
    """
    Retrieves a alumnus account by its unique identifier.

    Args:
        id (int): The unique ID of the alumnus account.

    Returns:
        Optional[AlumnusAccount]: The matching alumnus account if found, otherwise None.
    """
    return AlumnusAccount.get(id=id)


def get_alumnus_account_by_login_email(login_email: str) -> Optional[AlumnusAccount]:
    """
    Retrieves a alumnus account by its unique login email.

    Args:
        id (int): The unique login_email of the alumnus account.

    Returns:
        Optional[AlumnusAccount]: The matching alumnus account if found, otherwise None.
    """
    return AlumnusAccount.get(login_email=login_email)


"""
------ READ/GET (MULTIPLE RECORDS) ------
"""


def get_all_alumnus_accounts(jsonify_results: bool = False) -> Union[List[AlumnusAccount], List[dict]]:
    """
    Retrieves all alumnus accounts from the database.

    Args:
        jsonify_results (bool, optional): If True, returns alumnus accounts as a list of JSON-serializable dictionaries.
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


def get_alumnus_accounts_by_first_name(first_name: str, jsonify_results: bool = False) -> Union[List[AlumnusAccount], List[dict]]:
    """
    Retrieves all alumnus accounts with the given first name.

    Args:
        first_name (str): The alumnus' first name
        jsonify_results (bool, optional): If True, returns alumnus accounts as a list of JSON-serializable dictionaries.
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


def get_alumnus_accounts_by_last_name(last_name: str, jsonify_results: bool = False) -> Union[List[AlumnusAccount], List[dict]]:
    """
    Retrieves all alumnus accounts with the given last name.

    Args:
        first_name (str): The alumnus' last name
        jsonify_results (bool, optional): If True, returns alumnus accounts as a list of JSON-serializable dictionaries.
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


def get_alumnus_accounts_by_phone_number(phone_number: str, jsonify_results: bool = False) -> Union[List[AlumnusAccount], List[dict]]:
    """
    Retrieves all alumnus accounts with the given phone number.

    Args:
        phone number (str): The alumnus' phone number.
        jsonify_results (bool, optional): If True, returns alumnus accounts as a list of JSON-serializable dictionaries.
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
            phone_number=phone_number
        ),
        jsonify_results
    )


def get_alumnus_accounts_by_profile_photo_file_path(profile_photo_file_path: str, jsonify_results: bool = False) -> Union[List[AlumnusAccount], List[dict]]:
    """
    Retrieves all alumnus accounts with the given profile photo file path.

    Args:
        profile_photo_file_path (str): The file path to the alumnus's profile photo
        jsonify_results (bool, optional): If True, returns alumnus accounts as a list of JSON-serializable dictionaries.
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
------ UPDATE ------
"""


def update_alumnus_login_email(id: int, password: str, new_email: str) -> bool:
    """
    Updates the login email of an alumnus account after verifying their password.

    Args:
        id (int): The ID of the alumnus whose email is being updated.
        password (str): The current password to verify identity.
        new_email (str): The new email address to update.

    Returns:
        AlumnusAccount: The updated AlumnusAccount if successful.

    Raises:
        ValueError: If the alumnus id, new email, or password are empty or invalid.
        PermissionError: If the password is incorrect.
        IntegrityError: If the new email is already taken.
        SQLAlchemyError: For any other database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id <{id}> not found.")

    if not password:
        raise ValueError("Invalid password <[HIDDEN]>.")

    if not alumnus.check_password(password):
        raise PermissionError("Incorrect password <[HIDDEN]>.")

    if not (new_email and validate_email(new_email)):
        raise ValueError(f"Invalid email <'{new_email}'>.")

    try:
        alumnus.login_email = new_email
        db.session.commit()
        print("Login email updated successfully.")
        return alumnus

    except IntegrityError:
        db.session.rollback()
        raise IntegrityError("Error: Email address already in use.")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


def update_alumnus_password(id: int, password: str, new_password: str) -> bool:
    """
    Updates the password of an alumnus account after verifying their existing password.

    Args:
        id (int): The ID of the alumnus whose email is being updated.
        password (str): The current password to verify identity.
        new_password (str): The new password to update.

    Returns:
        AlumnusAccount: The updated AlumnusAccount if successful.

    Raises:
        ValueError: If the alumnus id, new email, or password are empty or invalid.
        PermissionError: If the password is incorrect.
        IntegrityError: If the new email is already taken.
        SQLAlchemyError: For any other database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id <{id}> not found.")

    if not password:
        raise ValueError("Invalid password <[HIDDEN]>.")

    if not alumnus.check_password(password):
        raise PermissionError("Incorrect password <[HIDDEN]>.")

    if not (new_password):
        raise ValueError(f"Invalid new password <'{new_password}'>.")

    try:
        alumnus.set_password(new_password)
        db.session.commit()
        print("Password updated successfully.")
        return alumnus

    except IntegrityError:
        db.session.rollback()
        raise IntegrityError("Error: Email address already in use.")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


def update_alumnus_first_name(id: int, new_first_name: str) -> bool:
    """
    Updates the first name of an alumnus account.

    Args:
        id (int): The ID of the alumnus whose email is being updated.
        new_first_name (str): The new first name to update.

    Returns:
        AlumnusAccount: The updated AlumnusAccount if successful.

    Raises:
        ValueError: If the alumnus id is invalid.
        SQLAlchemyError: For any database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id <{id}> not found.")

    try:
        alumnus.first_name = new_first_name
        db.session.commit()
        print("First name updated successfully.")
        return alumnus

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


def update_alumnus_last_name(id: int, new_last_name: str) -> bool:
    """
    Updates the last name of an alumnus account.

    Args:
        id (int): The ID of the alumnus whose email is being updated.
        new_last_name (str): The new last name to update.

    Returns:
        AlumnusAccount: The updated AlumnusAccount if successful.

    Raises:
        ValueError: If the alumnus id is invalid.
        SQLAlchemyError: For any database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id <{id}> not found.")

    try:
        alumnus.last_name = new_last_name
        db.session.commit()
        print("Last name updated successfully.")
        return alumnus

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


def update_alumnus_phone_number(id: int, new_phone_number: str) -> bool:
    """
    Updates the phone number of an alumnus account.

    Args:
        id (int): The ID of the alumnus whose email is being updated.
        new_phone_number (str): The new phone number to update.

    Returns:
        AlumnusAccount: The updated AlumnusAccount if successful.

    Raises:
        ValueError: If the alumnus id is invalid.
        SQLAlchemyError: For any database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id <{id}> not found.")

    try:
        alumnus.phone_number = new_phone_number
        db.session.commit()
        print("First name updated successfully.")
        return alumnus

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


def update_alumnus_profile_photo(id: int, new_profile_photo_file_path: str) -> bool:
    """
    Updates the profile photo of an alumnus account.

    Args:
        id (int): The ID of the alumnus whose email is being updated.
        new_profile_photo_file_path (str): The new profile photo's file path to update.

    Returns:
        AlumnusAccount: The updated AlumnusAccount if successful.

    Raises:
        ValueError: If the alumnus id is invalid.
        SQLAlchemyError: For any database-related issues.
    """
    alumnus = get_alumnus_account(id)
    if not alumnus:
        raise ValueError(f"Alumnus with id <{id}> not found.")

    try:
        alumnus.profile_photo_file_path = new_profile_photo_file_path
        db.session.commit()
        print("Profile photo updated successfully.")
        return alumnus

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


"""
------ DELETE
"""


def delete_alumnus_account(target_id: int, requester_id: int) -> None:
    """
    Securely deletes an alumnus account if the requester is an admin.

    Args:
        target_id (int): The ID of the alumnus account to delete.
        requester_id (int): The ID of the admin requesting the deletion.

    Raises:
        ValueError: If the targeted account does not exist, or the requester tries to delete themselves.
        PermissionError: If the requester is not an admin/does not exist.
        SQLAlchemyError: For any database-related issues.
    """
    if target_id == requester_id:
        raise ValueError(
            "Cannot request self-deletion. There must always be at least one alumnus.")

    alumnus_to_delete = get_alumnus_account(target_id)
    if not alumnus_to_delete:
        raise ValueError(
            f"Target alumnus account with id <{target_id}> not found")

    requesting_admin = AdminAccount.get(id=requester_id)
    if not requesting_admin:
        raise PermissionError(
            f"Requester admin account with id <{requester_id}> not found")

    try:
        db.session.delete(alumnus_to_delete)
        db.session.commit()
        print(f"Alumnus account with id <'{id}'> deleted successfully")

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deleting alumnus account with id <'{id}'>: {e}")


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


# def add_categories(id, job_categories):
#     alumni = get_alumni(id)
#     try:
#         for category in job_categories:
#             # print(category)
#             alumni.add_category(category)
#             # print(alumni.get_categories())
#             db.session.commit()
#         return alumni
#     except:
#         db.session.rollback()
#         return None


# def remove_categories(id, job_categories):
#     alumni = get_alumni(id)
#     try:
#         for category in job_categories:
#             alumni.remove_category(category)
#             db.session.commit()
#         return alumni
#     except:
#         db.session.rollback()
#         return None

# # apply to an application
# # def apply_listing(alumni_id, listing_title):


# def apply_listing(id, joblisting_id):
#     from App.controllers import get_listing, get_company_by_name

#     alumni = get_alumni(id)

#     # error check to see if alumni exists
#     if alumni is None:
#         # print('is none')
#         return None

#     # get the listing and then company that made the listing
#     listing = get_listing(joblisting_id)

#     if listing is None:
#         return None

#     # add the alumni to the listing applicant
#     listing.applicant.append(alumni)
#     alumni.listing.append(listing)

#     company = get_company_by_name(listing.company_name)

#     # commit changes to the database
#     db.session.commit()

#     listing.notify_observers(alumni, company)

#     # add the alumni as an applicant to the company model object?

#     return alumni


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


# def update_alumni_info(id, first_name, last_name, phone_number, login_email, current_password, new_password):
#     alumni = get_alumni(id)
#     update_made = False
#     # print("current password:")
#     # print (current_password)
#     # print("new password:")
#     # print(new_password)

#     if alumni.check_password(current_password):
#         if alumni.first_name != first_name:
#             alumni.first_name = first_name
#             print("first name updated")
#             update_made = True

#         if alumni.last_name != last_name:
#             alumni.last_name = last_name
#             print("last name updated")
#             update_made = True

#         if alumni.phone_number != phone_number:
#             alumni.phone_number = phone_number
#             print("phone number updated")
#             update_made = True

#         if alumni.login_email != login_email:
#             alumni.login_email = login_email
#             print("email updated")
#             update_made = True

#         if new_password:
#             alumni.set_password(new_password)
#             print("password updated")
#             update_made = True

#     if update_made:
#         db.session.commit()

#     return update_made


# def get_saved_listings(alumnus_id):
#     saved_listings = SavedJobListing.query.filter_by(
#         alumnus_id=alumnus_id).all()
#     return saved_listings


# def get_job_applications(alumnus_id):
#     job_applications = JobApplication.query.filter_by(
#         alumnus_id=alumnus_id).all()
#     return job_applications

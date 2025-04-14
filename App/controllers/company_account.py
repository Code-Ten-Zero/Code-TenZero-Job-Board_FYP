from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional, Union

from App.database import db
from App.models import BaseUserAccount, AdminAccount, CompanyAccount
from App.utils.db_utils import get_records_by_filter, validate_email

"""
===== CREATE =====
"""


def add_company_account(
        login_email: str, password: str, registered_name: str, mailing_address: str,
        public_email: str, website_url: str = None, phone_number: str = None,
        profile_photo_file_path: str = None
) -> CompanyAccount:
    """
    Adds a new company account to the database.

    Args:
        login_email (str): The unique email used to log into the company's account.
        password_hash (str): The hashed password for authentication.
        registered_name (str): The company's unique, government-registered name.
        mailing_address (str): The company's mailing address.
        public_email (str): The company's public contact email.
        website_url (str, optional): The company's unique official website URL.
        phone_number (str, optional): The company's unique phone number, which may include country codes and extensions.
        profile_photo_file_path (str, optional): The file path to the admin's profile photo.

    Returns:
        CompanyAccount: The newly added company account if successful.

    Raises:
        ValueError: If the input is invalid or the company was was not found.
        IntegrityError: If a database constraint is violated.
        SQLAlchemyError: For other database-related issues.
    """

    # Check for existing accounts with duplicate fields
    check_fields = {
        "login_email": login_email, "registered_name": registered_name,
        "phone_number": phone_number, "website_url": website_url
    }

    for field, value in check_fields.items():
        if value:
            for subclass in BaseUserAccount.__subclasses__():
                # Only check for existing value if the field exists
                if hasattr(subclass, field) and subclass.query.filter_by(**{field: value}).first():
                    raise ValueError(
                        f"{field.replace('_', ' ').title()} <'{value}'> already exists."
                    )

    new_company = CompanyAccount(
        login_email=login_email,
        password=password,
        registered_name=registered_name,
        mailing_address=mailing_address,
        public_email=public_email,
        website_url=website_url,
        phone_number=phone_number,
        profile_photo_file_path=profile_photo_file_path
    )

    try:
        db.session.add(new_company)
        db.session.commit()
        return new_company

    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


"""
===== READ/GET (SINGLE RECORD) =====
"""


def get_company_account(id: int) -> Optional[CompanyAccount]:
    """
    Retrieves a company account by its unique identifier.

    Args:
        id (int): The unique ID of the company account.

    Returns:
        Optional[CompanyAccount]: The matching company account if found, otherwise None.
    """
    return db.session.get(CompanyAccount, id)


def get_company_account_by_login_email(login_email: str) -> Optional[CompanyAccount]:
    """
    Retrieves a company account by its unique login email.

    Args:
        id (int): The unique login_email of the company account.

    Returns:
        Optional[CompanyAccount]: The matching company account if found, otherwise None.
    """
    return CompanyAccount.query.filter_by(login_email=login_email).first()


def get_company_account_by_registered_name(registered_name: str) -> Optional[CompanyAccount]:
    """
    Retrieves a company account by its unique registered name.

    Args:
        registered_name (str): The company's unique registered name

    Returns:
        Optional[CompanyAccount]: The matching company account if found, otherwise None.
    """
    return CompanyAccount.query.filter_by(registered_name=registered_name).first()


def get_company_account_by_phone_number(phone_number: str) -> Optional[CompanyAccount]:
    """
    Retrieves a company account by its unique phone number.

    Args:
        phone_number (str): The company's unique phone number

    Returns:
        Optional[CompanyAccount]: The matching company account if found, otherwise None.
    """
    return CompanyAccount.query.filter_by(phone_number=phone_number).first()


def get_company_account_by_website_url(website_url: str) -> Optional[CompanyAccount]:
    """
    Retrieves a company account by its unique website URL.

    Args:
        website_url (str): The company's unique registered name

    Returns:
        Optional[CompanyAccount]: The matching company account if found, otherwise None.
    """
    return CompanyAccount.query.filter_by(website_url=website_url).first()


"""
===== READ/GET (MULTIPLE RECORDS) =====
"""


def get_all_company_accounts(
        jsonify_results: bool = False
) -> Union[List[CompanyAccount], List[dict]]:
    """
    Retrieves all company accounts from the database.

    Args:
        jsonify_results (bool, optional):
            If True, returns company accounts as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[CompanyAccount], List[dict]]:
            - If `jsonify_results` is False, returns a list of `CompanyAccount` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no company accounts are found.
    """
    return get_records_by_filter(
        lambda: CompanyAccount.query.all(),
        jsonify_results
    )


def get_company_accounts_by_mailing_address(
        mailing_address: str, jsonify_results: bool = False
) -> Union[List[CompanyAccount], List[dict]]:
    """
    Retrieves all company accounts with the given mailing address.

    Args:
        mailing_address (str): The company's physical mailing address
        jsonify_results (bool, optional):
            If True, returns company accounts as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[CompanyAccount], List[dict]]:
            - If `jsonify_results` is False, returns a list of `CompanyAccount` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no company accounts are found.
    """
    return get_records_by_filter(
        lambda: CompanyAccount.query.filter_by(
            mailing_address=mailing_address
        ),
        jsonify_results
    )


def get_company_accounts_by_profile_photo_file_path(
        profile_photo_file_path: str, jsonify_results: bool = False
) -> Union[List[CompanyAccount], List[dict]]:
    """
    Retrieves all company accounts with the given profile photo file path.

    Args:
        profile_photo_file_path (str): The file path to the company's profile photo
        jsonify_results (bool, optional):
            If True, returns company accounts as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[CompanyAccount], List[dict]]:
            - If `jsonify_results` is False, returns a list of `CompanyAccount` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no company accounts are found.
    """
    return get_records_by_filter(
        lambda: CompanyAccount.query.filter_by(
            profile_photo_file_path=profile_photo_file_path
        ),
        jsonify_results
    )


"""
===== UPDATE =====
"""


def update_company_account_login_email(
        id: int, current_password: str, new_login_email: str
) -> CompanyAccount:
    """
    Securely updates the company's login email after verifying their current password.

    Args:
        id (int): The company's ID.
        current_password (str): The company's current password for authentication.
        new_login_email (str): The new login email.

    Returns:
        CompanyAccount: The updated company account if successful.

    Raises:
        ValueError: If the input is invalid or the company was not found.
        PermissionError: If the current password is incorrect.
        IntegrityError: If the new login email is already in use.
        SQLAlchemyError: For other database-related issues.
    """
    company = get_company_account(id)
    if not company:
        raise ValueError(f"Company with id {id} was not found.")

    if not current_password or not company.check_password(current_password):
        raise PermissionError("Incorrect password.")

    if not new_login_email or not validate_email(new_login_email):
        raise ValueError(f"Invalid email '{new_login_email}'.")

    try:
        company.login_email = new_login_email
        db.session.commit()
        return company

    except IntegrityError:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_company_account_password(
        id: int, current_password: str, new_password: str
) -> CompanyAccount:
    """
    Securely updates the company's password after verifying their current password.

    Args:
        id (int): The company's ID.
        current_password (str): The company's current password for authentication.
        new_password (str): The new password.

    Returns:
        CompanyAccount: The updated company account.

    Raises:
        ValueError: If the company id, new email, or password are empty or invalid.
        PermissionError: If the password is incorrect.
        SQLAlchemyError: For other database-related issues.
    """
    company = get_company_account(id)
    if not company:
        raise ValueError(f"Company with id {id} was not found.")

    if not current_password or not company.check_password(current_password):
        raise PermissionError("Incorrect password.")

    if not (new_password):
        raise ValueError("New password cannot be empty.")

    try:
        company.set_password(new_password)
        db.session.commit()
        return company

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_company_registered_name(id: int, new_registered_name: str) -> bool:
    """
    Updates the unique registered name of an company account.

    Args:
        id (int): The company's ID.
        new_registered_name (str): The new registered name.

    Returns:
        CompanyAccount: The updated company account if successful.

    Raises:
        ValueError: If the company id is invalid.
        IntegrityError: If the registered name is already taken.
        SQLAlchemyError: For any database-related issues.
    """
    company = get_company_account(id)
    if not company:
        raise ValueError(f"Company with id {id} was not found.")

    try:
        company.registered_name = new_registered_name
        db.session.commit()
        return company

    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_company_mailing_address(id: int, new_mailing_address: str) -> bool:
    """
    Updates the mailing address of an company account.

    Args:
        id (int): The company's ID.
        new_registered_name (str): The new mailing address.

    Returns:
        CompanyAccount: The updated company account if successful.

    Raises:
        ValueError: If the company id is invalid.
        SQLAlchemyError: For any database-related issues.
    """
    company = get_company_account(id)
    if not company:
        raise ValueError(f"Company with id {id} was not found.")

    try:
        company.mailing_address = new_mailing_address
        db.session.commit()
        return company

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_company_public_email(id: int, new_public_email: str) -> bool:
    """
    Updates the public contact email of an company account.

    Args:
        id (int): The company's ID.
        new_public_email (str): The public contact email.

    Returns:
        CompanyAccount: The updated company account if successful.

    Raises:
        ValueError: If the company id is invalid.
        SQLAlchemyError: For any database-related issues.
    """
    company = get_company_account(id)
    if not company:
        raise ValueError(f"Company with id {id} was not found.")

    try:
        company.public_email = new_public_email
        db.session.commit()
        return company

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_company_website_url(id: int, new_website_url: str) -> bool:
    """
    Updates the unique website URL of an company account.

    Args:
        id (int): The company's ID.
        new_website_url (str): The new website URL.

    Returns:
        CompanyAccount: The updated company account if successful.

    Raises:
        ValueError: If the company id is invalid.
        IntegrityError: If the website URL is already taken.
        SQLAlchemyError: For any database-related issues.
    """
    company = get_company_account(id)
    if not company:
        raise ValueError(f"Company with id {id} was not found.")

    try:
        company.website_url = new_website_url
        db.session.commit()
        return company

    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_company_phone_number(id: int, new_phone_number: str) -> bool:
    """
    Updates the unique phone number of an company account.

    Args:
        id (int): The company's ID.
        new_phone_number (str): The new phone number.

    Returns:
        CompanyAccount: The webupdated company account if successful.

    Raises:
        ValueError: If the company id is invalid.
        IntegrityError: If the website URL is already taken.
        SQLAlchemyError: For any database-related issues.
    """
    company = get_company_account(id)
    if not company:
        raise ValueError(f"Company with id {id} was not found.")

    try:
        company.phone_number = new_phone_number
        db.session.commit()
        return company

    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


def update_company_profile_photo(id: int, new_profile_photo_file_path: str) -> bool:
    """
    Updates the profile photo of an company account.

    Args:
        id (int): The company's ID.
        new_profile_photo_file_path (str): The new profile photo's file path.

    Returns:
        CompanyAccount: The webupdated company account if successful.

    Raises:
        ValueError: If the company id is invalid.
        SQLAlchemyError: For any database-related issues.
    """
    company = get_company_account(id)
    if not company:
        raise ValueError(f"Company with id {id} was not found.")

    try:
        company.profile_photo_file_path = new_profile_photo_file_path
        db.session.commit()
        return company

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


"""
===== DELETE
"""


def delete_company_account(target_id: int, requester_id: int) -> None:
    """
    Securely deletes an company account if the requester is an admin.

    Args:
        target_id (int): The ID of the company account to be deleted.
        requester_id (int): The ID of the admin requesting the deletion.

    Raises:
        ValueError: If the targeted account does not exist.
        PermissionError: If the requester does not exist or lacks permissions.
        SQLAlchemyError: For any database-related issues.
    """
    company_to_delete = get_company_account(target_id)
    if not company_to_delete:
        raise ValueError(
            f"Target company account with id {target_id} was not found")

    if not db.session.get(AdminAccount, requester_id):
        raise PermissionError(
            f"Requester (Admin ID {requester_id}) was was not found or lacks permissions."
        )

    try:
        db.session.delete(company_to_delete)
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occured: {e}")

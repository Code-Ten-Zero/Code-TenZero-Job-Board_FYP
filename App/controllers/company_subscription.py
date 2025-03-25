from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional, Union

from App.database import db
from App.models import AdminAccount, AlumnusAccount, CompanySubscription, CompanyAccount
from App.utils.db_utils import get_records_by_filter

"""
===== CREATE =====
"""


def add_company_subscription(alumnus_id: int, company_id: int) -> CompanySubscription:
    """
    Adds a new company subscription to the database.

    Args:
        alumnus_id (int): The ID of the alumnus subscribing.
        company_id (str): The company being subscribed to.

    Returns:
        CompanySubscription: The newly added company subscription if successful.

    Raises:
        ValueError: If the input is invalid or the queried records were not found.
        IntegrityError: If a database constraint is violated.
        SQLAlchemyError: For other database-related issues.
    """

    if not db.session.get(AlumnusAccount, alumnus_id):
        raise ValueError(f"Alumnus with id {id} not found")

    if not db.session.get(CompanyAccount, company_id):
        raise ValueError(f"Company with id {id} not found")

    new_saved_listing = CompanySubscription(
        alumnus_id=alumnus_id,
        company_id=company_id
    )

    try:
        db.session.add(new_saved_listing)
        db.session.commit()
        return new_saved_listing

    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


"""
===== READ/GET (SINGLE RECORD) =====
"""


def get_company_subscription(alumnus_id: int, company_id: int) -> Optional[CompanySubscription]:
    """
    Retrieves a company subscription by its unique alumnus-company ID combination.

    Args:
        alumnus_id (int): The unique ID of the subscribed alunmus.
        company_id (int): The unique ID of the subscribed-to company.

    Returns:
        Optional[CompanySubscription]: The matching company subscription if found, otherwise None.
    """
    return db.session.get(CompanySubscription, (alumnus_id, company_id))


"""
===== READ/GET (MULTIPLE RECORDS) =====
"""


def get_all_company_subscriptions(
        jsonify_results: bool = False
) -> Union[List[CompanySubscription], List[dict]]:
    """
    Retrieves all company subscriptions from the database.

    Args:
        jsonify_results (bool, optional):
            If True, returns company subscriptions as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[CompanySubscription], List[dict]]:
            - If `jsonify_results` is False, returns a list of `CompanySubscription` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no company subscriptions are found.
    """
    return get_records_by_filter(
        CompanySubscription,
        lambda: CompanySubscription.query.all(),
        jsonify_results
    )


def get_company_subscriptions_by_alumnus_id(
        alumnus_id: int, jsonify_results: bool = False
) -> Union[List[CompanySubscription], List[dict]]:
    """
    Retrieves all company subscriptions created by a given alumnus.

    Args:
        alumnus_id (int): The unique ID of the almnus that applied.
        jsonify_results (bool, optional):
            If True, returns company subscriptions as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[CompanySubscription], List[dict]]:
            - If `jsonify_results` is False, returns a list of `CompanySubscription` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no company subscriptions are found.
    """
    return get_records_by_filter(
        CompanySubscription,
        lambda: CompanySubscription.query.filter_by(alumnus_id=alumnus_id),
        jsonify_results
    )


def get_company_subscriptions_by_company_id(
        company_id: int, jsonify_results: bool = False
) -> Union[List[CompanySubscription], List[dict]]:
    """
    Retrieves all company subscriptions made for a given job listing.

    Args:
        company_id (int): The unique ID of the job listing that was applied for.
        jsonify_results (bool, optional):
            If True, returns company subscriptions as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[CompanySubscription], List[dict]]:
            - If `jsonify_results` is False, returns a list of `CompanySubscription` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no company subscriptions are found.
    """
    return get_records_by_filter(
        CompanySubscription,
        lambda: CompanySubscription.query.filter_by(alumnus_id=company_id),
        jsonify_results
    )


"""
===== DELETE
"""


def delete_company_subscription(
        alumnus_id: int, company_id: int, requester_id: int
) -> None:
    """
    Securely deletes an company subscription if the requester is an admin.

    Args:
        almunus_id (int): The ID of the alumnus that applied for the listing.
        company_id (int): The ID of the job listing applied to.
        requester_id (int): The ID of the admin requesting the deletion.

    Raises:
        ValueError: If the targeted company subscription does not exist.
        PermissionError: If the requester does not exist or lacks permissions.
        SQLAlchemyError: For any database-related issues.
    """
    saved_listing_to_delete = get_company_subscription(
        alumnus_id, company_id
    )
    if not saved_listing_to_delete:
        raise ValueError(
            f"Target company subscription with alumnus id {alumnus_id} and job listing id {company_id} was not found."
        )

    if not AdminAccount.get(id=requester_id):
        raise PermissionError(
            f"Requester (Admin ID {requester_id}) was was not found or lacks permissions."
        )

    try:
        db.session.delete(saved_listing_to_delete)
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occured: {e}")

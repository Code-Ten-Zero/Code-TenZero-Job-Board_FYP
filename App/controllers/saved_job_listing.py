from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional, Union

from App.database import db
from App.models import AdminAccount, AlumnusAccount, JobListing, SavedJobListing
from App.utils.db_utils import get_records_by_filter

"""
===== CREATE =====
"""


def add_saved_job_listing(alumnus_id: int, job_listing_id: int) -> SavedJobListing:
    """
    Adds a new saved job listing to the database.

    Args:
        alumnus_id (int): The ID of the alumnus saving the listing.
        job_listing_id (str): The job listing being saved.

    Returns:
        SavedJobListing: The newly added saved job listing if successful.

    Raises:
        ValueError: If the input is invalid or the queried records were not found.
        IntegrityError: If a database constraint is violated.
        SQLAlchemyError: For other database-related issues.
    """

    if not db.session.get(AlumnusAccount, alumnus_id):
        raise ValueError(f"Alumnus with id {id} not found")

    if not db.session.get(JobListing, job_listing_id):
        raise ValueError(f"Job listing with id {id} not found")

    new_saved_listing = SavedJobListing(
        alumnus_id=alumnus_id,
        job_listing_id=job_listing_id
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


def get_saved_job_listing(alumnus_id: int, job_listing_id: int) -> Optional[SavedJobListing]:
    """
    Retrieves a saved job listing by its unique alumnus-listing ID combination.

    Args:
        alumnus_id (int): The unique ID of the alunmus that saved the listing .
        job_listing_id (int): The unique ID of the job_listing that was saved.

    Returns:
        Optional[SavedJobListing]: The matching saved job listing if found, otherwise None.
    """
    return db.session.get(SavedJobListing, (alumnus_id, job_listing_id))


"""
===== READ/GET (MULTIPLE RECORDS) =====
"""


def get_all_saved_job_listings(
        jsonify_results: bool = False
) -> Union[List[SavedJobListing], List[dict]]:
    """
    Retrieves all saved job listings from the database.

    Args:
        jsonify_results (bool, optional):
            If True, returns saved job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[SavedJobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `SavedJobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no saved job listings are found.
    """
    return get_records_by_filter(
        SavedJobListing,
        lambda: SavedJobListing.query.all(),
        jsonify_results
    )


def get_saved_job_listings_by_alumnus_id(
        alumnus_id: int, jsonify_results: bool = False
) -> Union[List[SavedJobListing], List[dict]]:
    """
    Retrieves all saved job listings created by a given alumnus.

    Args:
        alumnus_id (int): The unique ID of the almnus that applied.
        jsonify_results (bool, optional):
            If True, returns saved job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[SavedJobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `SavedJobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no saved job listings are found.
    """
    return get_records_by_filter(
        SavedJobListing,
        lambda: SavedJobListing.query.filter_by(alumnus_id=alumnus_id),
        jsonify_results
    )


def get_saved_job_listings_by_job_listing_id(
        job_listing_id: int, jsonify_results: bool = False
) -> Union[List[SavedJobListing], List[dict]]:
    """
    Retrieves all saved job listings made for a given job listing.

    Args:
        job_listing_id (int): The unique ID of the job listing that was applied for.
        jsonify_results (bool, optional):
            If True, returns saved job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[SavedJobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `SavedJobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no saved job listings are found.
    """
    return get_records_by_filter(
        SavedJobListing,
        lambda: SavedJobListing.query.filter_by(alumnus_id=job_listing_id),
        jsonify_results
    )


"""
===== DELETE
"""


def delete_saved_job_listing(
        alumnus_id: int, job_listing_id: int, requester_id: int
) -> None:
    """
    Securely deletes an saved job listing if the requester is an admin.

    Args:
        almunus_id (int): The ID of the alumnus that applied for the listing.
        job_listing_id (int): The ID of the job listing applied to.
        requester_id (int): The ID of the admin requesting the deletion.

    Raises:
        ValueError: If the targeted saved job listing does not exist.
        PermissionError: If the requester does not exist or lacks permissions.
        SQLAlchemyError: For any database-related issues.
    """
    saved_listing_to_delete = get_saved_job_listing(
        alumnus_id, job_listing_id
    )
    if not saved_listing_to_delete:
        raise ValueError(
            f"Target saved job listing with alumnus id {alumnus_id} and job listing id {job_listing_id} was not found."
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

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional, Union

from App.database import db
from App.models import AdminAccount, CompanyAccount, JobListing
from App.utils.db_utils import get_records_by_filter

"""
===== CREATE =====
"""


def add_job_listing(
        company_id: int, title: str, position_type: str,
        description: str, monthly_salary_ttd: int,
        is_remote: bool = False, job_site_address: str = None
) -> JobListing:
    """
    Adds a new job listing to the database.

    Args:
        company_id (int): The ID of the company posting the job.
        title (str): The job title.
        position_type (str): The type of the position (e.g., Full-time, Part-time).
        description (str): A description of the job.
        monthly_salary_ttd (int): The monthly salary in TTD (Trinidad and Tobago Dollars).
        is_remote (bool, optional): Whether the job is remote. Defaults to False.
        job_site_address (str, optional): The address of the job site, if applicable. Defaults to None.

    Returns:
        JobListing: The newly added job listing if successful.

    Raises:
        ValueError: If the input is invalid or the company was was not found.
        IntegrityError: If a database constraint is violated.
        SQLAlchemyError: For other database-related issues.
    """

    if not db.session.get(CompanyAccount, company_id):
        raise ValueError(f"Company with id {id} not found")

    if monthly_salary_ttd <= 0:
        raise ValueError(
            "Monthly salary cannot be less than or equal to $0 TTD.")

    new_company = JobListing(
        company_id=company_id,
        title=title,
        position_type=position_type,
        description=description,
        monthly_salary_ttd=monthly_salary_ttd,
        is_remote=is_remote,
        job_site_address=job_site_address
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


def get_job_listing(id: int) -> Optional[JobListing]:
    """
    Retrieves a job listing by its unique identifier.

    Args:
        id (int): The unique ID of the job listing.

    Returns:
        Optional[JobListing]: The matching job listing if found, otherwise None.
    """
    return db.session.get(JobListing, id)


"""
===== READ/GET (MULTIPLE RECORDS) - EXACT MATCH =====
"""


def get_all_job_listings(
        jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves all job listings from the database.

    Args:
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.all(),
        jsonify_results
    )


def get_job_listings_by_company_id(
        company_id: int, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves all job listings created by a company with a given ID.

    Args:
        company_id (int): The unique ID of the company that created the job listing
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter_by(company_id=company_id),
        jsonify_results
    )


def get_job_listings_by_exact_title(
        job_title: str, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves all job listings that match the provided title exactly.

    Args:
        job_title (str): The exact job title to search for.
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no similar job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter_by(title=job_title),
        jsonify_results
    )


def get_job_listings_by_exact_position_type(
        position_type: str, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves all job listings that match the provided position type exactly.

    Args:
        position_type (str): The exact position type to search for.
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no similar job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter_by(position_type=position_type),
        jsonify_results
    )


def get_job_listings_by_exact_description(
        description: str, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves all job listings that match the provided description exactly.

    Args:
        description (str): The exact description to search for.
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no similar job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter_by(description=description),
        jsonify_results
    )


def get_job_listings_by_monthly_salary_ttd(
        monthly_salary_ttd: int, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves all job listings that offer a given monthly salary.

    Args:
        monthly_salary_ttd (str): The monthly salary (in TTD) to search for.
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no similar job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter_by(
            monthly_salary_ttd=monthly_salary_ttd
        ),
        jsonify_results
    )


def get_job_listings_by_is_remote(
        is_remote: bool, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves all job listings that match the given remote working flag.

    Args:
        is_remote (str): The remote working flag to search for.
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no similar job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter_by(
            is_remote=is_remote
        ),
        jsonify_results
    )


def get_job_listings_by_job_site_address(
        job_site_address: str, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves all job listings that match the given physical jobsite address exactly.

    Args:
        job_site_address (str): The exact physical jobsite address to search for.
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no similar job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter_by(
            job_site_address=job_site_address
        ),
        jsonify_results
    )


"""
===== READ/GET (MULTIPLE RECORDS) - SIMILAR MATCH =====
"""


def get_job_listings_by_similar_title(
        job_title: str, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves all job listings with titles that are similar to the provided title.

    Args:
        job_title (str): The job title to search for similar listings.
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no similar job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter(
            JobListing.title.ilike(f"%{job_title}%")
        ),
        jsonify_results
    )


def get_job_listings_by_similar_position_type(
        position_type: str, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves job listings with similar position types.

    Args:
        position_type (str): The position type to search for similar listings.
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no similar job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter(
            JobListing.position_type.ilike(f"%{position_type}%")
        ),
        jsonify_results
    )


def get_job_listing_by_similar_description(
        description: str, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves job listings with similar descriptions.

    Args:
        description (str): The description to search for similar listings.
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no similar job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter(
            JobListing.description.ilike(f"%{description}%")),
        jsonify_results
    )


def get_job_listing_by_similar_job_site_address(
        job_site_address: str, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves job listings with similar physical jobsite addresses.

    Args:
        job_site_address (str): The jobsite address to search for similar listings.
        jsonify_results (bool, optional):
            If True, returns job listings as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobListing], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobListing` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no similar job listings are found.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter(
            JobListing.job_site_address.ilike(f"%{job_site_address}%")),
        jsonify_results
    )


"""
===== READ/GET (MULTIPLE RECORDS) - RANGE =====
"""


def get_job_listings_by_salary_range(
    min_monthly_salary_ttd: float, max_monthly_salary_ttd: float, jsonify_results: bool = False
) -> Union[List[JobListing], List[dict]]:
    """
    Retrieves job listings that offer a salary within the specified range.

    Args:
        min_monthly_salary_ttd (float): The minimum monthly salary (in TTD) to filter by.
        max_monthly_salary_ttd (float): The maximum monthly salary (in TTD) to filter by.
        jsonify_results (bool, optional): If True, returns results as JSON.

    Returns:
        List[JobListing] or List[dict]: A list of job listings within the given salary range.
    """
    return get_records_by_filter(
        lambda: JobListing.query.filter(
            JobListing.monthly_salary_ttd >= min_monthly_salary_ttd,
            JobListing.monthly_salary_ttd <= max_monthly_salary_ttd
        ),
        jsonify_results
    )


"""
===== UPDATE =====
"""


def update_job_listing_title(
        id: int, new_title: str
) -> JobListing:
    """
    Updates the job listing's title.

    Args:
        id (int): The job listing's ID.
        new_title (str): The new title.

    Returns:
        JobListing: The updated job listing if successful.

    Raises:
        ValueError: If the input is invalid or the job listing was not found.
        SQLAlchemyError: For other database-related issues.
    """
    listing = get_job_listing(id)
    if not listing:
        raise ValueError(f"Job listing with id {id} was not found.")

    if not new_title:
        raise ValueError(f"Invalid title '{new_title}'.")

    try:
        listing.title = new_title
        db.session.commit()
        return listing

    except IntegrityError:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_job_listing_position_type(
        id: int, new_position_type: str
) -> JobListing:
    """
    Updates the job listing's position type.

    Args:
        id (int): The job listing's ID.
        new_position_type (str): The new position type.

    Returns:
        JobListing: The updated job listing.

    Raises:
        ValueError: If the input is invalid or the job listing was not found.
        SQLAlchemyError: For other database-related issues.
    """
    listing = get_job_listing(id)
    if not listing:
        raise ValueError(f"Job listing with id {id} was not found.")

    if not (new_position_type):
        raise ValueError("New position type cannot be empty.")

    try:
        listing.position_type = new_position_type
        db.session.commit()
        return listing

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_job_listing_description(id: int, new_description: str) -> JobListing:
    """
    Updates the job listing's description.

    Args:
        id (int): The job listing's ID.
        new_description (str): The new description.

    Returns:
        JobListing: The updated job listing if successful.

    Raises:
        ValueError: If the input is invalid or the job listing was not found.
        SQLAlchemyError: For any database-related issues.
    """
    listing = get_job_listing(id)
    if not listing:
        raise ValueError(f"Job listing with id {id} was not found.")

    if not new_description:
        raise ValueError("New description cannot be empty.")

    try:
        listing.registered_name = new_description
        db.session.commit()
        return listing

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_job_listing_monthly_salary_ttd(id: int, new_monthly_salary_ttd: int) -> JobListing:
    """
    Updates the job listing's monthly salary (in TTD).

    Args:
        id (int): The job listing's ID.
        new_monthly_salary_ttd (str): The new monthly salary (in TTD).

    Returns:
        JobListing: The updated job listing if successful.

    Raises:
        ValueError: If the input is invalid or the job listing was not found.
        SQLAlchemyError: For any database-related issues.
    """
    listing = get_job_listing(id)
    if not listing:
        raise ValueError(f"Job listing with id {id} was not found.")

    if new_monthly_salary_ttd <= 0:
        raise ValueError(
            "Monthly salary cannot be less than or equal to $0 TTD.")

    try:
        listing.monthly_salary_ttd = new_monthly_salary_ttd
        db.session.commit()
        return listing

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_job_listing_is_remote(id: int, new_is_remote: bool = False) -> JobListing:
    """
    Updates the job listing's is_remote flag.

    Args:
        id (int): The job listing's ID.
        new_is_remote (str): The new is_remote flag. Defaults to False

    Returns:
        JobListing: The updated job listing if successful.

    Raises:
        ValueError: If the job listing was not found.
        SQLAlchemyError: For any database-related issues.
    """
    listing = get_job_listing(id)
    if not listing:
        raise ValueError(f"Job listing with id {id} was not found.")

    try:
        listing.is_remote = new_is_remote
        db.session.commit()
        return listing

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def update_job_listing_job_site_address(id: int, new_job_site_address: str = None) -> JobListing:
    """
    Updates the job listing's physical jobsite address.

    Args:
        id (int): The job listing's ID.
        new_job_site_address (str): The new job site address. Defaults to None

    Returns:
        JobListing: The updated job listing if successful.

    Raises:
        ValueError: If the job listing was not found.
        SQLAlchemyError: For any database-related issues.
    """
    listing = get_job_listing(id)
    if not listing:
        raise ValueError(f"JobListing with id {id} was not found.")

    try:
        listing.job_site_address = new_job_site_address
        db.session.commit()
        return listing

    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def approve_job_listing(id: int) -> JobListing:
    """
    Updates the job listing's approval status to "APPROVED".

    Args:
        id (int): The job listing's ID.

    Returns:
        JobListing: The updated job listing if successful.

    Raises:
        ValueError: If the job listing was not found.
        SQLAlchemyError: For any database-related issues.
    """
    listing = get_job_listing(id)
    if not listing:
        raise ValueError(f"JobListing with id {id} was not found.")

    try:
        listing.admin_approval_status = "APPROVED"
        db.session.commit()
        return listing

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def unapprove_job_listing(id: int) -> JobListing:
    """
    Updates the job listing's approval status to "PENDING".

    Args:
        id (int): The job listing's ID.

    Returns:
        JobListing: The updated job listing if successful.

    Raises:
        ValueError: If the job listing was not found.
        SQLAlchemyError: For any database-related issues.
    """
    listing = get_job_listing(id)
    if not listing:
        raise ValueError(f"JobListing with id {id} was not found.")

    try:
        listing.admin_approval_status = "PENDING"
        db.session.commit()
        return listing

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


def get_approved_listings():
    all_listings = JobListing.query.all()
    my_approved_listings = []
    for listing in all_listings:
        if listing.admin_approval_status == "APPROVED":
            my_approved_listings.append(listing)
    return my_approved_listings


def toggle_listing_approval(listing_id, status):
    print("toggle listing approval function")
    from .job_listing import get_listing

    listing = get_listing(listing_id)
    if not listing:
        return None
    if status in ["APPROVED", "PENDING", "REJECTED"]:
        listing.admin_approval_status = status
    else:
        return None

    try:
        db.session.commit()
        return True
    except Exception as e:
        print(f'my error: {e}')
        db.session.rollback()
        return None


"""
===== DELETE
"""


def delete_job_listing(target_id: int, requester_id: int) -> None:
    """
    Securely deletes an job listing if the requester is an admin.

    Args:
        target_id (int): The ID of the job listing to be deleted.
        requester_id (int): The ID of the admin requesting the deletion.

    Raises:
        ValueError: If the targeted account does not exist.
        PermissionError: If the requester does not exist or lacks permissions.
        SQLAlchemyError: For any database-related issues.
    """
    listing_to_delete = get_job_listing(target_id)
    if not listing_to_delete:
        raise ValueError(
            f"Target job listing with id {target_id} was not found")

    if not db.session.get(AdminAccount, requester_id):
        raise PermissionError(
            f"Requester (Admin ID {requester_id}) was was not found or lacks permissions."
        )

    try:
        db.session.delete(listing_to_delete)
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occured: {e}")

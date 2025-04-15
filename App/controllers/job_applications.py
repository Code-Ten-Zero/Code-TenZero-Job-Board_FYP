from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional, Union

from App.database import db
from App.models import AdminAccount, AlumnusAccount, JobApplication, JobListing
from App.utils.db_utils import get_records_by_filter

"""
===== CREATE =====
"""


def add_job_application(
        alumnus_id: int, job_listing_id: int,
        resume_file_path: str
) -> JobApplication:
    """
    Adds a new job application to the database.

    Args:
        alumnus_id (int): The ID of the alumnus applying for the job.
        job_listing_id (str): The job listing beign applied for.
        resume_file_path (str): The file path to the applicant's uploaded resume.

    Returns:
        JobApplication: The newly added job application if successful.

    Raises:
        ValueError: If the input is invalid or the queried records were not found.
        IntegrityError: If a database constraint is violated.
        SQLAlchemyError: For other database-related issues.
    """

    if not db.session.get(AlumnusAccount, alumnus_id):
        raise ValueError(f"Alumnus with id {id} not found")

    if not db.session.get(JobListing, job_listing_id):
        raise ValueError(f"Job listing with id {id} not found")

    if not resume_file_path:
        raise ValueError(
            "Resume file path cannot be empty."
        )

    new_application = JobApplication(
        alumnus_id=alumnus_id,
        job_listing_id=job_listing_id,
        resume_file_path=resume_file_path
    )

    try:
        db.session.add(new_application)
        db.session.commit()
        return new_application

    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError(f"A database constraint was violated: {e}")

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {e}")


"""
===== READ/GET (SINGLE RECORD) =====
"""


def get_job_application(alumnus_id: int, job_listing_id: int) -> Optional[JobApplication]:
    """
    Retrieves a job application by its unique alumnus-listing ID combination.

    Args:
        alumnus_id (int): The unique ID of the alunmus who applied.
        job_listing_id (int): The unique ID of the job_listing.

    Returns:
        Optional[JobApplication]: The matching job application if found, otherwise None.
    """
    return db.session.get(JobApplication, (alumnus_id, job_listing_id))


"""
===== READ/GET (MULTIPLE RECORDS) =====
"""


def get_all_job_applications(
        jsonify_results: bool = False
) -> Union[List[JobApplication], List[dict]]:
    """
    Retrieves all job applications from the database.

    Args:
        jsonify_results (bool, optional):
            If True, returns job applications as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobApplication], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobApplication` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no job applications are found.
    """
    return get_records_by_filter(
        lambda: JobApplication.query.all(),
        jsonify_results
    )


def get_job_applications_by_alumnus_id(
        alumnus_id: int, jsonify_results: bool = False
) -> Union[List[JobApplication], List[dict]]:
    """
    Retrieves all job applications created by a given alumnus.

    Args:
        alumnus_id (int): The unique ID of the almnus that applied.
        jsonify_results (bool, optional):
            If True, returns job applications as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobApplication], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobApplication` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no job applications are found.
    """
    return get_records_by_filter(
        lambda: JobApplication.query.filter_by(alumnus_id=alumnus_id),
        jsonify_results
    )


def get_job_applications_by_job_listing_id(
        job_listing_id: int, jsonify_results: bool = False
) -> Union[List[JobApplication], List[dict]]:
    """
    Retrieves all job applications made for a given job listing.

    Args:
        job_listing_id (int): The unique ID of the job listing that was applied for.
        jsonify_results (bool, optional):
            If True, returns job applications as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobApplication], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobApplication` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no job applications are found.
    """
    return get_records_by_filter(
        lambda: JobApplication.query.filter_by(alumnus_id=job_listing_id),
        jsonify_results
    )


def get_job_applications_by_resume_file_path(
        resume_file_path: str, jsonify_results: bool = False
) -> Union[List[JobApplication], List[dict]]:
    """
    Retrieves all job applications made using the same resume file.

    Args:
        resume_file_path (str): The file path of the alumnus' resume.
        jsonify_results (bool, optional):
            If True, returns job applications as a list of JSON-serializable dictionaries.
            Defaults to False.

    Returns:
        Union[List[JobApplication], List[dict]]:
            - If `jsonify_results` is False, returns a list of `JobApplication` objects.
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
            - Returns an empty list if no similar job applications are found.
    """
    return get_records_by_filter(
        lambda: JobApplication.query.filter_by(
            resume_file_path=resume_file_path
        ),
        jsonify_results
    )


"""
===== UPDATE =====
"""


def update_job_application_resume_file_path(
        alumnus_id: int, job_listing_id: int, new_resume_file_path: str
) -> JobApplication:
    """
    Updates the resume attached to the job application.

    Args:
        almunus_id (int): The ID of the alumnus that applied for the listing.
        job_listing_id (int): The ID of the job listing applied to.
        resume_file_path (str): The file path of the resume.

    Returns:
        JobApplication: The updated job application if successful.

    Raises:
        ValueError: If the input is invalid or the job application was not found.
        SQLAlchemyError: For other database-related issues.
    """
    application = get_job_application(alumnus_id, job_listing_id)
    if not application:
        raise ValueError(
            f"Job application with alumnus id {alumnus_id} and job listing id {job_listing_id} was not found."
        )

    if not new_resume_file_path:
        raise ValueError(f"Invalid title '{new_resume_file_path}'.")

    try:
        application.resume_file_path = new_resume_file_path
        db.session.commit()
        return application

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occurred: {e}")


"""
===== DELETE
"""


def delete_job_application(
        alumnus_id: int, job_listing_id: int, requester_id: int
) -> None:
    """
    Securely deletes an job application if the requester is an admin.

    Args:
        almunus_id (int): The ID of the alumnus that applied for the listing.
        job_listing_id (int): The ID of the job listing applied to.
        requester_id (int): The ID of the admin requesting the deletion.

    Raises:
        ValueError: If the targeted job application does not exist.
        PermissionError: If the requester does not exist or lacks permissions.
        SQLAlchemyError: For any database-related issues.
    """
    application_to_delete = get_job_application(alumnus_id, job_listing_id)
    if not application_to_delete:
        raise ValueError(
            f"Target job application with alumnus id {alumnus_id} and job listing id {job_listing_id} was not found."
        )

    if not db.session.get(AdminAccount, requester_id):
        raise PermissionError(
            f"Requester (Admin ID {requester_id}) was was not found or lacks permissions."
        )

    try:
        db.session.delete(application_to_delete)
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(f"A database error has occured: {e}")

from datetime import datetime
from flask import current_app
from sqlalchemy.orm import validates
from App.database import db


class JobApplication(db.Model):
    """
    Represents an application made by an alumnus to a given job listing.

    Attributes:
        id (int): A unique identifier for the job application.
        alumnus_id (int): Foreign key referencing the alumnus applying for the job.
        job_listing_id (int): Foreign key referencing the company hosting the job listing.
        resume_file_path (str): The file path to the attached resume.
        datetime_applied (datetime): When the application was created.
        company_approval_status (str): Whether the company has approved the application (e.g., "PENDING", "APPROVED").

        alumnus (relationship): Many-to-one relationship to the 'AlumnusAccount' model.
        job_listing (relationship): Many-to-one relationship to the 'JobListings' model.

    Note: See config file for valid approval statuses.
    """

    __tablename__ = "job_applications"

    id = db.Column(db.Integer(), primary_key=True)
    alumnus_id = db.Column(db.Integer, db.ForeignKey(
        'alumnus.id'), nullable=False)
    job_listing_id = db.Column(db.Integer, db.ForeignKey(
        'job_listing.id'), nullable=False)
    resume_file_path = db.Column(db.String, nullable=False)
    datetime_applied = db.Column(
        db.DateTime, nullable=False, default=datetime.now(datetime.timezone.utc))
    company_approval_status = db.Column(
        db.String(50), nullable=False, default="PENDING")

    alumni = db.relationship(
        "AlumnusAccount", back_populates="job_applications")
    job_listings = db.relationship(
        "JobListing", back_populates='job_applications')

    __table_args__ = (
        db.CheckConstraint(
            f"company_approval_status IN ({', '.join(repr(s) for s in current_app.config['APPROVAL_STATUSES'])})", name="valid_approval_status"),
    )

    def __init__(self, alumnus_id: int, job_listing_id: int, resume_file_path: str) -> None:
        """
        Initializes a JobApplication instance.

        Args:
            alumnus_id (int): ID of the alumnus applying for the job.
            job_listing_id (int): ID of the job listing being applied to.
            resume_file_path (str): The file path to the attached resume.
        """
        self.alumnus_id = alumnus_id
        self.job_listing_id = job_listing_id
        self.resume_file_path = resume_file_path

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the job application.

        Returns:
            str: A formatted string displaying job application details.
        """
        return f"""{self.__class__.__name__} Info:
    - ID: {self.id}
    - Alumnus ID: {self.alumnus_id}
    - Job Listing ID: {self.job_listing_id}
    - Resume File Path: {self.resume_file_path}
    - Date/Time Applied: {self.datetime_applied.isoformat()}
    - Company Approval Status = {self.company_approval_status}
    """

    def __repr__(self) -> str:
        """
        Returns a developer-friendly representation of the job application.

        Returns:
            str: A string containing the job application details.
        """
        return (f"<{self.__class__.__name__} (id={self.id}, alumnus_id={self.alumnus_id}, "
                f"job_listing_id='{self.job_listing_id}'], resume_file_path='{self.resume_file_path}', "
                f"datetime_applied='{self.datetime_applied.isoformat()}, "
                f"company_approval_status='{self.company_approval_status}')>")

    def __json__(self):
        """
        Returns a JSON-serializable representation of the job application.

        Returns:
            dict: A dictionary containing job application details.
        """
        return {
            "id": {self.id},
            "alumnus_id": {self.alumnus_id},
            "job_listing_id": {self.job_listing_id},
            "resume_file_path": {self.resume_file_path},
            "datetime_applied": {self.datetime_applied.isoformat()},
            "company_approval_status": {self.company_approval_status}
        }

    @validates("company_approval_status")
    def validate_approval_status(self, value: str) -> str:
        """
        Ensures that 'company_approval_status' is valid.

        Args:
            key (str): The column being validated.
            value (str): The value assigned to 'approval_status'.

        Returns:
            str: Validated value.

        Raises:
            ValueError: If the status is invalid.
        """
        valid_statuses = current_app.config["APPROVAL_STATUSES"]
        if value not in valid_statuses:
            raise ValueError(
                f"Invalid status '{value}'. Allowed values: {valid_statuses}")
        return value

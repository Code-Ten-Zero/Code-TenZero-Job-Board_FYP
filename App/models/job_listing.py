from datetime import datetime
from flask import current_app
from sqlalchemy.orm import validates
from App.database import db


class JobListing(db.Model):
    """
    Represents a job listing made by a given company.

    Attributes:
        id (int): A unique identifier for the job listing.
        company_id (str): Foreign key referencing the company posting the job.
        title (str): The job title.
        position_type (str): The type of employment (e.g., "FULL-TIME", "CONTRACT").
        description (str): Job requirements and details.
        monthly_salary_ttd: Monthly salary in Trinidad and Tobago Dollars.
        is_remote (bool): Indicates if the job is remote (False by default).
        job_site_address (str): Physical address of the job site (automatically set to "N/A" when is_remote is True).
        datetime_created (datetime): When the job listing was created.
        datetime_last_modified (datetime): When the job listing was last modified.
        admin_approval_status (str): Whether an admin has approved the job listing (e.g., "PENDING", "APPROVED").

        company (relationship): Many-to-one relationship to the 'CompanyAccount' model.
        job_applications (relationship): One-to-many relationship to the 'JobApplication' model.
        saved_job_listings (relationship): One-to-many relationship to the 'SavedJobListing' model.

    Note: See config file for valid position types and approval statuses.
    """

    __tablename__ = "job_listings"

    id = db.Column(db.Integer(), primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'company_accounts.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    position_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    monthly_salary_ttd = db.Column(db.Integer, nullable=False)
    is_remote = db.Column(db.Boolean, nullable=False, default=False)
    job_site_address = db.Column(db.String(120), nullable=False)
    datetime_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_approval_status = db.Column(
        db.String(50), nullable=False, default="PENDING")

    company = db.relationship("CompanyAccount", back_populates="job_listings")
    job_applications = db.relationship(
        "JobApplication", back_populates='job_listing', lazy="dynamic", cascade="all, delete-orphan")
    saved_job_listings = db.relationship(
        "SavedJobListing", back_populates='job_listing', lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, company_id: int, title: str, position_type: str, description: str, monthly_salary_ttd: int, is_remote: bool = False, job_site_address: str = None,  datetime_created=None, datetime_last_modified=None, admin_approval_status: str = 'PENDING') -> None:
        """
        Initializes a JobListing instance.

        Args:
            company_id (int): ID of the company posting the job.
            title (str): Job title.
            position_type (str): Type of employment (e.g., "FULL-TIME", "CONTRACT").
            description (str): Job description.
            monthly_salary_ttd (int): Monthly salary in Trinidad and Tobago Dollars.
            is_remote (bool): Whether the job is remote (False by default).
            job_site_address (str): Physical address of the job site (automatically set to "N/A" if is_remote is True, CANNOT be "N/A" if is_remote is False).
        """
        self.company_id = company_id
        self.title = title
        self.position_type = position_type
        self.description = description
        self.monthly_salary_ttd = monthly_salary_ttd
        self.is_remote = is_remote
        self.job_site_address = "(Not specified)" if not job_site_address else ("N/A" if self.is_remote else job_site_address)
        self.datetime_created = datetime.utcnow()
        self.datetime_last_modified = datetime.utcnow()
        self.admin_approval_status = admin_approval_status

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the job listing.

        Returns:
            str: A formatted string displaying job listing details.
        """
        return f"""{self.__class__.__name__} Info:
    - ID: {self.id}
    - Company ID: {self.company_id}
    - Job Title: {self.title}
    - Position Type: {self.position_type}
    - Job Description: {self.description}
    - Monthly Salary (TTD): {self.monthly_salary_ttd}
    - Is Remote: {self.is_remote}
    - Job Site Address: {self.job_site_address}
    - Date/Time Created: {self.datetime_created.isoformat()}
    - Date/Time Last Modified: {self.datetime_last_modified.isoformat()}
    - Admin Approval Status: {self.admin_approval_status}
    """

    def __repr__(self) -> str:
        """
        Returns a developer-friendly representation of the job listing.

        Returns:
            str: A string containing the job listing details.
        """
        return (f"<{self.__class__.__name__} (id={self.id}, company_id={self.company_id}, "
                f"title='{self.title}', position_type='{self.position_type}', "
                f"description='{self.description}', monthly_salary_ttd={self.monthly_salary_ttd}, "
                f"is_remote={self.is_remote}, job_site_address='{self.job_site_address}', "
                f"datetime_created='{self.datetime_created.isoformat()}', "
                f"datetime_last_modified='{self.datetime_last_modified.isoformat()}, "
                f"admin_approval_status='{self.admin_approval_status}')>")

    def __json__(self):
        """
        Returns a JSON-serializable representation of the job listing.

        Returns:
            dict: A dictionary containing job listing details.
        """
        return {
            "id": self.id,
            "company_id": self.company_id,
            "title": self.title,
            "position_type": self.position_type,
            "description": self.description,
            "monthly_salary_ttd": self.monthly_salary_ttd,
            "is_remote": self.is_remote,
            "job_site_address": self.job_site_address,
            "datetime_created": self.datetime_created.isoformat(),
            "datetime_last_modified": self.datetime_last_modified.isoformat(),
            "admin_approval_status": self.admin_approval_status
        }
    # was causing errors revise-CTZ
    # @validates("admin_approval_status")
    # def validate_admin_approval_status(self, value: str) -> str:
    #     """
    #     Ensures that 'approval_status' is valid.

    #     Args:
    #         value (str): The value assigned to 'admin_approval_status'.

    #     Returns:
    #         str: Validated value.

    #     Raises:
    #         ValueError: If the status is invalid.
    #     """
    #     valid_statuses = current_app.config["APPROVAL_STATUSES"]
    #     if value not in valid_statuses:
    #         raise ValueError(f"Invalid status '{value}'. Allowed values: {valid_statuses}")
    #     return value

    @validates("is_remote", "job_site_address")
    def validate_job_site_address(self, key, value):
        """
        Ensures job_site_address is 'N/A' when is_remote is True.
        If job_site_address is given, is_remote is set to False.
        """
        if key == "is_remote" and value:  # If is_remote is set to True
            self.job_site_address = "N/A"

        if key == "job_site_address" and value != "N/A":  # If a job site address is provided
            self.is_remote = False

        return value

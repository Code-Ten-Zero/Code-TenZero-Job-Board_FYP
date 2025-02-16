from datetime import datetime
from flask import current_app
from sqlalchemy.orm import validates
from App.database import db


class JobApplication(db.Model):
    """
    Represents an application made by an alumnus to a given job listing.
    """

    __tablename__ = "job_applications"

    id = db.Column(db.Integer(), primary_key=True)
    alumnus_id = db.Column(db.Integer, db.ForeignKey('alumnus_accounts.id'), nullable=False)
    job_listing_id = db.Column(db.Integer, db.ForeignKey('job_listings.id'), nullable=False)
    resume_file_path = db.Column(db.String, nullable=False)
    datetime_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    company_approval_status = db.Column(db.String(50), nullable=False, default="PENDING")

    alumnus = db.relationship("AlumnusAccount", back_populates="job_applications")
    job_listing = db.relationship("JobListing", back_populates='job_applications')

    @validates("company_approval_status")
    def validate_approval_status(self, key, value: str) -> str:
        """
        Ensures that 'company_approval_status' is valid.
        """
        valid_statuses = current_app.config["APPROVAL_STATUSES"]
        if value not in ApprovalStatus._value2member_map_:
            raise ValueError(
                f"Invalid status '{value}'. Allowed values: {[status.value for status in ApprovalStatus]}")
        return value

    def __init__(self, alumnus_id: int, job_listing_id: int, resume_file_path: str) -> None:
        self.alumnus_id = alumnus_id
        self.job_listing_id = job_listing_id
        self.resume_file_path = resume_file_path

    def __str__(self) -> str:
        return f"""{self.__class__.__name__} Info:
    - ID: {self.id}
    - Alumnus ID: {self.alumnus_id}
    - Job Listing ID: {self.job_listing_id}
    - Resume File Path: {self.resume_file_path}
    - Date/Time Applied: {self.datetime_applied.isoformat()}
    - Company Approval Status = {self.company_approval_status}
    """

    def __repr__(self) -> str:
        return (f"<{self.__class__.__name__} (id={self.id}, alumnus_id={self.alumnus_id}, "
                f"job_listing_id='{self.job_listing_id}'], resume_file_path='{self.resume_file_path}', "
                f"datetime_applied='{self.datetime_applied.isoformat()}, "
                f"company_approval_status='{self.company_approval_status}')>")

    def __json__(self):
        return {
            "id": self.id,
            "alumnus_id": self.alumnus_id,
            "job_listing_id": self.job_listing_id,
            "resume_file_path": self.resume_file_path,
            "datetime_applied": self.datetime_applied.isoformat(),
            "company_approval_status": self.company_approval_status
        }

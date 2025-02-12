from flask import current_app
from App.database import db


class SavedJobListing(db.Model):
    """
    Represents a job listing saved (but not applied to) by a given alumnus.

    Attributes:
        alumnus_id (int): Foreign key referencing the alumnus saving the job listing.
        job_listing_id (int): Foreign key referencing the job listing being saved.

        alumnus (relationship): Many-to-one relationship to the 'AlumnusAccount' model.
        job_listing (relationship): Many-to-one relationship to the 'JobListing' model.

    Note: See config file for valid position types and approval statuses.
    """

    __tablename__ = "job_listings"

    alumnus_id = db.Column(db.Integer, db.ForeignKey('alumnus.id'), primary_key=True)
    job_listing_id = db.Column(db.Integer, db.ForeignKey('job_listing.id'), primary_key=True)
    
    alumnus = db.relationship("AlumnusAccount", back_populates="saved_job_listings")
    job_listing = db.relationship("JobListing", back_populates="saved_job_listings")

    def __init__(self, alumnus_id: int, job_listing_id: int) -> None:
        """
        Initializes a SavedJobListing instance.

        Args:
            alumnus_id (int): ID of the alumnus saving the job listing.
            job_listing_id (int): ID of the job listing being saved.
        """
        self.alumnus_id = alumnus_id
        self.job_listing_id = job_listing_id

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the saved job listing.

        Returns:
            str: A formatted string displaying saved job listing details.
        """
        return f"""{self.__class__.__name__} Info:
    - Alumnus ID: {self.alumnus_id}
    - Job Listing ID: {self.job_listing_id}
    """

    def __repr__(self) -> str:
        """
        Returns a developer-friendly representation of the saved job listing.

        Returns:
            str: A string containing the saved job listing details.
        """
        return (f"<{self.__class__.__name__} (alumnus_id={self.alumnus_id}, job_listing_id={self.job_listing_id})>")

    def __json__(self):
        """
        Returns a JSON-serializable representation of the job listing.

        Returns:
            dict: A dictionary containing job listing details.
        """
        return {
            "alumnus_id": {self.alumnus_id},
            "job_listing_id": {self.job_listing_id}
        }

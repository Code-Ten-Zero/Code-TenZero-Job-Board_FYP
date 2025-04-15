from sqlalchemy.orm import validates
from App.database import db


class SavedJobListing(db.Model):
    __tablename__ = "saved_job_listings"  # Corrected table name

    alumnus_id = db.Column(db.Integer, db.ForeignKey(
        'alumnus_accounts.id'), primary_key=True)
    job_listing_id = db.Column(db.Integer, db.ForeignKey(
        'job_listings.id'), primary_key=True)

    alumnus = db.relationship(
        "AlumnusAccount", back_populates="saved_job_listings")
    job_listing = db.relationship(
        "JobListing", back_populates="saved_job_listings")

    def __init__(self, alumnus_id: int, job_listing_id: int) -> None:
        self.alumnus_id = alumnus_id
        self.job_listing_id = job_listing_id

    def __str__(self) -> str:
        return f"""{self.__class__.__name__} Info:
    - Alumnus ID: {self.alumnus_id}
    - Job Listing ID: {self.job_listing_id}
    """

    def __repr__(self) -> str:
        return (f"<{self.__class__.__name__} (alumnus_id={self.alumnus_id}, job_listing_id={self.job_listing_id})>")

    def __json__(self):
        return {
            "alumnus_id": {self.alumnus_id},
            "job_listing_id": {self.job_listing_id}
        }

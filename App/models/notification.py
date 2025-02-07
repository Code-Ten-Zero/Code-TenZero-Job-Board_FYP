from datetime import datetime
from App.database import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed = db.Column(db.Boolean, default=False, nullable=False)
    
    # Foreign key relationships
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=True)
    
    # # Relationships
    # company = db.relationship('Company', back_populates='notifications')
    # listing = db.relationship('Listing', back_populates='notifications')

    def __repr__(self):
        return f"<Notification(id={self.id}, message={self.message},created_at = {self.created_at} , reviewed={self.reviewed})>"

    def json(self):
        return {
            "id": self.id,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
            "reviewed": self.reviewed,
            "admin_id": self.admin_id,
	        "alumni_id": self.alumni_id,
	        "company_id" : self.company_id,
            "listing_id" : self.listing_id

        }

from datetime import datetime
from App.database import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed = db.Column(db.Boolean, default=False, nullable=False)
    
    # Foreign key relationships (here from the previous code)
    user_account_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # (here from the previous code)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    
    # Relationships 
    # company = db.relationship('Company', back_populates='notifications')
    # listing = db.relationship('Listing', back_populates='notifications')

    def __repr__(self):
        return f"<Notification(id={self.id}, message={self.message},created_at = {self.created_at} ,user_account_id={self.user_account_id}, reviewed={self.reviewed})>"

    def json(self):
        return {
            "id": self.id,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
            "reviewed": self.reviewed,
	    "user_account_id": self.user_account_id,
	    "company_id" : self.company_id,
            "listing_id" : self.listing_id

        }
from datetime import datetime
from App.database import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key relationships
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    
    # # Relationships
    # company = db.relationship('Company', back_populates='notifications')
    # listing = db.relationship('Listing', back_populates='notifications')
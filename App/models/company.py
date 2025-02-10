from App.database import db
from .user import User
from .observer import Observer

class Company(User, Observer):

    company_name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(30), nullable=True)
    mailing_address = db.Column(db.String(120), nullable=True)
    public_email = db.Column(db.String(120), nullable=True)
    website_url = db.Column(db.String(120), nullable=True)

    # Relationship with notifications
    # One-to-many relationship with Notification
    notifications = db.relationship('Notification', backref='company', lazy=True)

    # set up relationship with Listing object (1-M)
    listings = db.relationship('Listing', backref='company', lazy=True)

    def __init__(self, company_name, password, email, mailing_address, public_email, phone_number, website_url):
        super().__init__(password, email)
        self.company_name = company_name
        self.mailing_address = mailing_address
        self.public_email = public_email
        self.phone_number = phone_number
        self.website_url = website_url
        
    def get_json(self):
        return{
            'id': self.id,
            'company_name': self.company_name,
            'email': self.email,
            'public_email': self.public_email,
            'mailing_address':self.mailing_address,
            'phone_number':self.phone_number,
            'website_url':self.website_url
        }
    
    def get_name(self):
        return self.company_name

    def update(self, alumni, listing):
        """Handle notification when an alumni applies to a listing."""
        print(f"Alumni {alumni.username} applied to your listing '{listing.title}'.")
    
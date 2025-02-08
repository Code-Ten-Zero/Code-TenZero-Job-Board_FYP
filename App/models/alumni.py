from App.database import db
from .user import User
from .listing import categories

# from .file import File

# categories = ['Software Engineering', 'Database', 'Programming', 'N/A']

class Alumni(User):
    # inherits ID from User
    #alumni_id = db.Column(db.Integer, nullable = False, unique = True)

    #name
    firstname = db.Column(db.String(120), nullable = False)
    lastname = db.Column(db.String(120), nullable = False)
    phone_number = db.Column(db.String(30), nullable = True)

    # Define relationship to listings
    listing = db.relationship('Listing', secondary='alumni_listings', back_populates='applicant')

    # relationship to listings to receive notifications?
    subscribed = db.Column(db.Boolean, default=False)


    def __init__(self, password, email, phone_number, firstname, lastname):
        super().__init__(username, password, email)
        self.subscribed = False
        self.phone_number = phone_number
        self.firstname = firstname
        self.lastname = lastname

    def get_alumni_id(self):
        return self.id

    def get_json(self):
        return{
            'id': self.id,
            'email': self.email,
            'subscribed': self.subscribed,
            'phone_number':self.phone_number,
            'firstname':self.firstname,
            'lastname':self.lastname
        }
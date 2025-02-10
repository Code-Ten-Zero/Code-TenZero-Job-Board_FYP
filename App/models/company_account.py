from App.database import db
from .base_user_account import BaseUserAccount


class CompanyAccount(BaseUserAccount):
    """
    Represents a company account in the system.

    This class extends 'BaseUserAccount' to store company-specific 
    details, including contact information and job listings.

    Attributes:
        id (int): A unique identifier for the company account.
        email (str): The company's email address, used for authentication.
        password_hash (str): The hashed version of the company's password.
        company_name (str): The registered name of the company (must be unique).
        mailing_address (str): The company's mailing address.
        website_url (str, optional): The company's website URL (must be unique if provided).
        phone_number (str, optional): The company's contact number, which may include country codes and extensions.

    Relationships:
        notifications (relationship): One-to-many relationship with the 'Notification' model.
        job_listings (relationship): One-to-many relationship with the 'JobListing' model.
    """

    __tablename__ = "company_accounts"

    __mapper_args__ = {
        'polymorphic_identity': 'company',
    }

    company_name = db.Column(db.String, nullable=False, unique=True)
    mailing_address = db.Column(db.String, nullable=False)
    website_url = db.Column(db.String, nullable=True, unique=True)

    # Phone number is stored as a string to accommodate international formats and extensions
    phone_number = db.Column(db.String, nullable=True, unique=True)

    job_listings = db.relationship('JobListing', back_populates='company',)

    def __init__(self, email: str, password: str, company_name: str, mailing_address: str, website_url: str = None, phone_number: str = None) -> None:
        """
        Initializes a new 'CompanyAccount' instance.

        Args:
            email (str): The company's email address, used for authentication (must be unique).
            password (str): The company's plaintext password (hashed internally before storage).
            company_name (str): The registered name of the company (must be unique).
            mailing_address (str): The company's mailing address.
            website_url (str, optional): The company's official website URL.
            phone_number (str, optional): The company's contact number. Example: "+1-(868)-123-4567 ext. 8910"
        """
        super().__init__(email, password)
        self.company_name = company_name
        self.mailing_address = mailing_address
        self.website_url = website_url
        self.phone_number = phone_number

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the company account.

        Returns:
            str: A formatted string displaying company account details (excluding password hash).
        """
        return f"""{self.__class__.__name__} Info:
    - ID: {self.id}
    - Email: {self.email}
    - Password Hash: [HIDDEN]
    - Company Name: {self.company_name}
    - Mailing Address: {self.mailing_address}
    - Website URL: {self.website_url if self.website_url else "N/A"}
    - Phone Number: {self.phone_number if self.phone_number else "N/A"}
    """

    def __repr__(self) -> str:
        """
        Returns a developer-friendly representation of the company account.

        Returns:
            str: A string containing company account details (excluding password hash).
        """
        return (f"<{self.__class__.__name__} (id={self.id}, email='{self.email}', "
                f"password_hash='[HIDDEN]', company_name='{self.company_name}', "
                f"mailing_address='{self.mailing_address}', "
                f"website_url='{self.website_url if self.website_url else '[N/A]'}', "
                f"phone_number='{self.phone_number if self.phone_number else '[N/A]'}')>")

    def __json__(self) -> dict:
        """
        Returns a JSON-serializable representation of the company account.

        Returns:
            dict: A dictionary containing company account details (excluding password hash).
        """
        return {
            'id': self.id,
            'email': self.email,
            'password_hash': "[HIDDEN]",
            'company_name': self.company_name,
            'mailing_address': self.mailing_address,
            'website_url': self.website_url if self.website_url else None,
            'phone_number': self.phone_number if self.phone_number else None
        }

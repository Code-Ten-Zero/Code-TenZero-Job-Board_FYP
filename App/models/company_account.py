from App.database import db
from .base_user_account import BaseUserAccount


class CompanyAccount(BaseUserAccount):
    """
    Represents a company account, inheriting from the base user class.

    Attributes:
        id (int): A unique identifier for the company account.
        login_email (str): The unique email used to log into the company's account.
        password_hash (str): The hashed password for authentication.
        registered_name (str): The company's unique, government-registered name.
        mailing_address (str): The company's mailing address.
        public_email (str): The company's public contact email.
        website_url (str, optional): The company's unique official website URL.
        phone_number (str, optional): The company's unique phone number, which may include country codes and extensions.
        profile_photo_file_path (str, optional): The file path to the admin's profile photo.

        notifications (relationship): One-to-many relationship with the 'Notification' model (inherited from base user class).
        job_listings (relationship): One-to-many relationship with the 'JobListing' model.
        subscribed_alumni (relationship): One-to-many relationship with the 'CompanySubscription' model.
    """

    __tablename__ = "company_accounts"

    __mapper_args__ = {
        'polymorphic_identity': 'company',
    }

    notifications = db.relationship(
        "Notification", back_populates="company", lazy="dynamic", cascade="all, delete-orphan")

    registered_name = db.Column(db.String, nullable=False, unique=True)
    mailing_address = db.Column(db.String, nullable=False)
    public_email = db.Column(db.String, nullable=False)
    website_url = db.Column(db.String, unique=True)

    # Phone number is stored as a string to accommodate international formats and extensions
    phone_number = db.Column(db.String, unique=True)

    job_listings = db.relationship(
        'JobListing', back_populates='company', lazy="dynamic", cascade="all, delete-orphan")
    subscribed_alumni = db.relationship(
        'CompanySubscription', back_populates='company', lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, login_email: str, password: str, registered_name: str, mailing_address: str, public_email: str, website_url: str = None, phone_number: str = None, profile_photo_file_path: str = None) -> None:
        """
        Initializes a new 'CompanyAccount' instance.

        Args:
            login_email (str): The unqiue email used to log into the company's account.
            password (str): The company's plaintext password (hashed internally before storage).
            registered_name (str): The company's unique, government-registered name.
            mailing_address (str): The company's mailing address.
            public_email (str): The company's public contact email.
            website_url (str, optional): The company's unique official website URL.
            phone_number (str, optional): The company's unique phone number. Example: "+1-(868)-123-4567 ext. 8910"
            profile_photo_file_path (str, optional): The file path to the admin's profile photo.
        """
        super().__init__(login_email, password, profile_photo_file_path)
        self.registered_name = registered_name
        self.mailing_address = mailing_address
        self.public_email = public_email
        self.website_url = website_url
        self.phone_number = phone_number
        self.profile_photo_file_path = 'profile-images/anonymous-profile.png'

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the company account.

        Returns:
            str: A formatted string displaying company account details (excluding password hash).
        """
        return f"""{self.__class__.__name__} Info:
    - ID: {self.id}
    - Login Email: {self.login_email}
    - Password Hash: [HIDDEN]
    - Registered Company Name: {self.registered_name}
    - Mailing Address: {self.mailing_address}
    - Public Email: {self.public_email}
    - Website URL: {self.website_url if self.website_url else "N/A"}
    - Phone Number: {self.phone_number if self.phone_number else "N/A"}
    - Profile Photo File Path: {self.profile_photo_file_path if self.profile_photo_file_path else "N/A"}
    """

    def __repr__(self) -> str:
        """
        Returns a developer-friendly representation of the company account.

        Returns:
            str: A string containing company account details (excluding password hash).
        """
        return (f"<{self.__class__.__name__} (id={self.id}, login_email='{self.login_email}', "
                f"password_hash='[HIDDEN]', registered_name='{self.registered_name}', "
                f"mailing_address='{self.mailing_address}', public_email='{self.public_email}', "
                f"website_url='{self.website_url if self.website_url else '[N/A]'}', "
                f"phone_number='{self.phone_number if self.phone_number else '[N/A]'}', "
                f"profile_photo_file_path='{self.profile_photo_file_path if self.profile_photo_file_path else 'N/A'}')>")

    def __json__(self) -> dict:
        """
        Returns a JSON-serializable representation of the company account.

        Returns:
            dict: A dictionary containing company account details (excluding password hash).
        """
        return {
            'id': self.id,
            'Login Email': self.login_email,
            'password_hash': "[HIDDEN]",
            'registered_name': self.registered_name,
            'mailing_address': self.mailing_address,
            'public_email': self.public_email,
            'website_url': self.website_url if self.website_url else None,
            'phone_number': self.phone_number if self.phone_number else None,
            'profile_photo_file_path': self.profile_photo_file_path if self.profile_photo_file_path else None
        }

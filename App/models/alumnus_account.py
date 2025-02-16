from App.database import db
from .base_user_account import BaseUserAccount


class AlumnusAccount(BaseUserAccount):
    """
    Represents an alumnus account, inheriting from the base user class.

    Attributes:
        id (int): A unique identifier for the alumnus account.
        login_email (str): The unique email used to log into the alumnus' account.
        password_hash (str): The hashed password for authentication.
        first_name (str): The alumnus' first name.
        last_name (str): The alumnus' last name.
        phone_number (str, optional): The alumnus' unique phone number, which may include country codes and extensions.
        profile_photo_file_path (str, optional): The file path to the admin's profile photo.

        notifications (relationship): One-to-many relationship with the 'Notification' model (inherited from base user class).
        job_applications (relationship): One-to-many relationship with the 'JobApplications' model.
        saved_job_listings (relationship): One-to-many relationship with the 'SavedJobListings' model.
        company_subscriptions (relationship): One-to-many relationship with the 'CompanySubscriptions' model.

    """

    __tablename__ = "alumnus_accounts"

    __mapper_args__ = {
        "polymorphic_identity": "alumnus"
    }

    notifications = db.relationship("Notification", back_populates="alumnus", lazy="dynamic", cascade="all, delete-orphan")

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    # String-type used to account for leading '0' and/or '+' in country codes, as well as format separators and extensions (e.g., "+1-(800)-555-1234 ext. 7890")
    phone_number = db.Column(db.String, unique=True)

    job_applications = db.relationship(
        'JobApplication', back_populates='alumnus', lazy="dynamic", cascade="all, delete-orphan")
    saved_job_listings = db.relationship(
        'SavedJobListing', back_populates='alumnus', lazy="dynamic", cascade="all, delete-orphan")
    company_subscriptions = db.relationship(
        'CompanySubscription', back_populates='alumnus', lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, login_email: str, password: str, first_name: str, last_name: str, phone_number: str = None, profile_photo_file_path: str = None) -> None:
        """
        Initializes a new alumnus account.

        Args:
            login_email (str): The unique email used to log into the admin's account.
            password (str): The alumnus' plaintext password (hashed internally before storage).
            first_name (str): The alumnus' first name.
            last_name (str): The alumnus' last name.
            phone_number (str, optional): The alumnus' unique phone number. Example: "+1-(868)-123-4567 ext. 8910"
            profile_photo_file_path (str, optional): The file path to the alumnus' profile photo.
        """
        super().__init__(login_email, password, profile_photo_file_path)
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the alumnus account.

        Returns:
            str: A formatted string displaying alumnus account details (excluding password hash).
        """
        return f"""{self.__class__.__name__} Info:
    - ID: {self.id}
    - Login Email: {self.login_email}
    - Password Hash: [HIDDEN]
    - First Name: {self.first_name}
    - Last Name: {self.last_name}
    - Phone Number: {self.phone_number if self.phone_number else 'N/A'}
    - Profile Photo File Path: {self.profile_photo_file_path if self.profile_photo_file_path else 'N/A'} 
    """

    def __repr__(self) -> str:
        """
        Returns a developer-friendly representation of the alumnus account.

        Returns:
            str: A string containing the alumnus account details (excluding password hash).
        """
        return (f"<{self.__class__.__name__} (id={self.id}, login_email='{self.login_email}', "
                f"password_hash='[HIDDEN]', first_name='{self.first_name}', "
                f"last_name='{self.last_name}', "
                f"phone_number='{self.phone_number if self.phone_number else 'N/A'}', "
                f"profile_photo_file_path='{self.profile_photo_file_path if self.profile_photo_file_path else 'N/A'}')>")

    def __json__(self) -> dict:
        """
        Returns a JSON-serializable representation of the alumnus account.

        Returns:
            dict: A dictionary containing alumnus account details (excluding password hash).
        """
        return {
            'id': self.id,
            'login_email': self.login_email,
            'password_hash': "[HIDDEN]",
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number if self.phone_number else None,
            'profile_photo_file_path': self.profile_photo_file_path if self.profile_photo_file_path else None
        }

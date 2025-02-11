from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class BaseUserAccount(db.Model):
    """
    Base class for user accounts, providing authentication features.

    This class is abstract and should be inherited by specific user types.
    It supports password hashing and verification.

    Attributes:
        id (int): A unique identifier for the user account.
        login_email (str): The unique email address used to log in to the user's account.
        password_hash (str): The hashed version of the user's password.
        profile_photo_file_path (str, optional): The file path to the user's profile photo.

        notifications (relationship): One-to-many relationship with the 'Notification' model.
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    login_email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(120), nullable=False)

    notifications = db.relationship(
        'Notification', back_populates='users', lazy="dynamic", cascade="all, delete-orphan")

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __init__(self, login_email: str, password: str, profile_photo_file_path: str = None) -> None:
        """
        Initialize a new BaseUserAccount.

        Args:
            login_email (str): The unique email used to log into the user's account.
            password (str): The user's plaintext password (will be hashed).
            profile_photo_file_path (str, optional): The file path to the user's profile photo.
        """
        self.login_email = login_email
        self.set_password(password)
        self.profile_photo_file_path = profile_photo_file_path if profile_photo_file_path else None

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the user account.

        Returns:
            str: A formatted string with user details (excluding password hash).
        """
        return f"""{self.__class__.__name__} Info:
    - ID: {self.id}
    - Email: {self.email}
    - Password Hash: [HIDDEN]
    - Profile Photo File Path: {self.profile_photo_file_path if self.profile_photo_file_path else "N/A"}
    """

    def __repr__(self) -> str:
        """
        Returns a developer-friendly representation of the user account.

        Returns:
            str: A string containing the class name, ID, and email.
        """
        return f"<{self.__class__.__name__} (id={self.id}, email='{self.email}', password_hash='[HIDDEN]', profile_photo_file_path='{self.profile_photo_file_path if self.profile_photo_file_path else 'N/A'}')>"

    def __json__(self) -> dict:
        """
        Returns a JSON-serializable representation of the user account.

        Returns:
            dict: A dictionary containing user details (excluding password hash).
        """
        return {
            'id': self.id,
            'email': self.email,
            'password_hash': "[HIDDEN]",
            'profile_photo_file_path': self.profile_photo_file_path if self.profile_photo_file_path else None
        }

    @property
    def password(self) -> None:
        """
        Prevent direct access to the password attribute.

        Raises:
            AttributeError: Always raises an error to prevent access.
        """
        raise AttributeError(
            "Password is not accessible directly. Use set_password() or check_password() instead.")

    @password.setter
    def password(self, password: str) -> None:
        """
        Stores a hash of the given plaintext password.

        Args:
            password (str): The plaintext password.
        """
        self.set_password(password)

    def set_password(self, password: str):
        """
        Stores a hash of the given plaintext password.

        Args:
            password (str): The plaintext password.
        """
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password: str) -> bool:
        """
        Verifies if the provided password (when hashed) matches the stored hash.

        Args:
            password (str): The plaintext password to verify.

        Returns:
            bool: True if the password hash matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

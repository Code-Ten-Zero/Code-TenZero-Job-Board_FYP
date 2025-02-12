from App.database import db
from .base_user_account import BaseUserAccount


class AdminAccount(BaseUserAccount):
    """
    Represents an admin account, inherting from the base user class.

    Attributes:
        login_email (str): The unique email used to log into the admin's account.
        password_hash (str): The hashed password for authentication.
        profile_photo_file_path (str, optional): The file path to the admin's profile photo.

        notifications (relationship): One-to-many relationship with the 'Notification' model (inherited from base user class).
    """

    __tablename__ = "admin_accounts"

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, login_email: str, password: str, profile_photo_file_path: str = None) -> None:
        """
        Initialize a new AdminAccount instance.

        Args:
            login_email (str): The unique email used to log into the admin's account.
            password (str): The admin's plaintext password (hashed internally before storage).
            profile_photo_file_path (str, optional): The file path to the admin's profile photo.
        """
        super().__init__(login_email, password, profile_photo_file_path)

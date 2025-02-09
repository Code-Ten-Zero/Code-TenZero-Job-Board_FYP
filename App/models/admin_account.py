from App.database import db
from .base_user_account import BaseUserAccount


class AdminAccount(BaseUserAccount):
    """
    Represents an admin account in the system.

    This class is a subclass of `BaseUserAccount` and provides specific 
    functionality for admin users. It supports authentication features, 
    including password hashing and verification.

    Attributes:
        email (str): The admin's email address.
        password_hash (str): The hashed password for authentication.
    """

    __tablename__ = "admin_accounts"

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, email: str, password: str) -> None:
        """
        Initialize a new AdminAccount instance.

        Inherited from `BaseUserAccount`, this constructor initializes the
        email and sets the password by hashing it.

        Args:
            email (str): The admin's email address.
            password (str): The plaintext password provided by the admin
                            (will be hashed for storage).
        """
        super().__init__(email, password)

from App.database import db
from .base_user_account import BaseUserAccount


class AlumnusAccount(BaseUserAccount):
    """
    Represents an alumnus account, inheriting from the base user class.

    
    Attributes:
        id (int): A unique identifier for the alumnus account.
        email (str): The alumnus' email address, used for authentication.
        password_hash (str): The hashed version of the alumnus' password.
        first_name (str): The alumnus' first name.
        last_name (str): The alumnus' last name.
        phone_number (str, optional): The alumnus' phone number, which may include country codes and extensions.

    Relationships:
        This model extends BaseUserAccount and does not define additional relationships directly.
    """

    __tablename__ = "alumnus_accounts"

    __mapper_args__ = {
        "polymorphic_identity": "alumnus"
    }

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    # String-type used to account for leading '0' and/or '+' in country codes, as well as format separators and extensions (e.g., "+1-(800)-555-1234 ext. 7890")
    phone_number = db.Column(db.String, nullable=True)

    def __init__(self, email: str, password: str, first_name: str, last_name: str, phone_number: str = None) -> None:
        """
        Initializes a new alumnus account.

        Args:
            email (str): The alumnus' email address (must be unique).
            password (str): The alumnus' plaintext password (hashed internally before storage).
            first_name (str): The alumnus' first name.
            last_name (str): The alumnus' last name.
            phone_number (str, optional): The alumnus' phone number. Example: "+1-(868)-123-4567 ext. 8910"
        """
        super().__init__(email, password)
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number if phone_number else "N/A"

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the alumnus account.

        Returns:
            str: A formatted string displaying alumnus account details (excluding password hash).
        """
        return f"""{self.__class__.__name__} Info:
    - ID: {self.id}
    - Email: {self.email}
    - Password Hash: [HIDDEN]
    - First Name: {self.first_name}
    - Last Name: {self.last_name}
    - Phone Number: {self.phone_number if self.phone_number else 'N/A'}
    """

    def __repr__(self) -> str:
        """
        Returns a developer-friendly representation of the alumnus account.

        Returns:
            str: A string containing the alumnus account details (excluding password hash).
        """
        return (f"<{self.__class__.__name__} (id={self.id}, email='{self.email}', "
                f"password_hash='[HIDDEN]', first_name='{self.first_name}', "
                f"last_name='{self.last_name}', "
                f"phone_number={self.phone_number if self.phone_number else 'N/A'})>")

    def __json__(self) -> dict:
        """
        Returns a JSON-serializable representation of the alumnus account.

        Returns:
            dict: A dictionary containing alumnus account details (excluding password hash).
        """
        return {
            'id': self.id,
            'email': self.email,
            'password_hash': "[HIDDEN]",
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number if self.phone_number else None
        }

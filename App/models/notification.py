from datetime import datetime
from App.database import db


class Notification(db.Model):
    """
    Represents a notification delivered to a user account.

    Attributes:
        id (int): A unique identifier for the notification.
        alumnus_id (str): Foreign key referencing the alumnus receiving the notification.
        company_id (str): Foreign key referencing the company receiving the notification.
        admin_id (str): Foreign key referencing the admin receiving the notification.
        message (str): The message the user will read.
        datetime_created (datetime): When the notification was created.
        reviewed_by_user (bool): Whether the user has opened/read the notification (defaults to False).

    """
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    alumnus_id = db.Column(db.Integer, db.ForeignKey(
        'alumnus_accounts.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'company_accounts.id'), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey(
        'admin_accounts.id'), nullable=True)
    message = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow)
    reviewed_by_user = db.Column(db.Boolean, default=False, nullable=False)

    alumnus = db.relationship("AlumnusAccount", back_populates="notifications")
    company = db.relationship("CompanyAccount", back_populates="notifications")
    admin = db.relationship("AdminAccount", back_populates="notifications")

    def __init__(self, alumnus_id: int, company_id: int, admin_id: int, message: str) -> None:
        """
        Initializes a Notification instance.

        Args:

            message (str): Notification message.
        """
        if alumnus_id:
            self.alumnus_id = alumnus_id
            self.company_id = None
            self.admin_id = None
            self.message = message

        elif company_id:
            self.company_id = company_id
            self.alumnus_id = None
            self.admin_id = None
            self.message = message

        elif admin_id:
            self.admin_id = admin_id
            self.alumnus_id = None
            self.company_id = None
            self.message = message

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the notification.

        Returns:
            str: A formatted string displaying job listing details.
        """
        return f"""{self.__class__.__name__} Info:
    - ID: {self.id}
    - Alumnus ID: {self.alumnus_id}
    - Company ID: {self.company_id}
    - Admin ID: {self.company_id}
    - Message: {self.message}
    - Date/Time Created: {self.datetime_created.isoformat()}
    - Reviewed By User: {self.reviewed_by_user}
    """

    def __repr__(self) -> str:
        """
        Returns a developer-friendly representation of the notification.

        Returns:
            str: A string containing the notification details.
        """
        return (f"<(id={self.id}, alumnus_id={self.alumnus_id}, company_id={self.company_id}, admin_id={self.admin_id}, "
                f"message='{self.message}', "
                f"datetime_created='{self.datetime_created.isoformat()}', "
                f"reviewed_by_user='{self.reviewed_by_user}')>")

    def __json__(self):
        return {
            "id": self.id,
            "Alumnus ID": {self.alumnus_id},
            "Company ID": {self.company_id},
            "Admin ID": {self.company_id},
            "message": self.message,
            "created_at": self.created_at.isoformat(),
            "reviewed_by_user": self.reviewed_by_user
        }

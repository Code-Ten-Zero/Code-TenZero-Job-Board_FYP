from datetime import datetime
from App.database import db


class Notification(db.Model):
    """
    Represents a notification delivered to a user account.

    Attributes:
        id (int): A unique identifier for the notification.
        user_id (str): Foreign key referencing the user recieving the notification.
        message (str): The message the user will read.
        datetime_created (datetime): When the notification was created.
        reviewed_by_user (bool): Whether the user has opened/read the notification (defaults to False).

        user (relationship): Many-to-one relationship to the 'BaseUserAccount' model.
    """
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow)
    reviewed_by_user = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship("BaseUserAccount", back_populates='notifications')

    def __init__(self, user_id: int, message: str) -> None:
        """
        Initializes a Notification instance.

        Args:
            user_id (int): ID of the user recieving the notification.
            message (str): Notification message.
        """
        self.user_id = user_id
        self.message = message

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the notification.

        Returns:
            str: A formatted string displaying job listing details.
        """
        return f"""{self.__class__.__name__} Info:
    - ID: {self.id}
    - User ID: {self.user_id}
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
        return (f"<(id={self.id}, user_id={self.user_id}, "
                f"message='{self.message}', "
                f"datetime_created='{self.datetime_created.isoformat()}', "
                f"reviewed_by_user='{self.reviewed_by_user}')>")
    
    def __json__(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
            "reviewed_by_user": self.reviewed_by_user
        }

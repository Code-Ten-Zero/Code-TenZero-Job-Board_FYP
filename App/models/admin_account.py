from App.database import db
from .base_user_account import BaseUserAccount


class AdminAccount(BaseUserAccount):
    __tablename__ = "admin_accounts"

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    notifications = db.relationship(
        "Notification", back_populates="admin", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, login_email: str, password: str, profile_photo_file_path: str = None) -> None:
        super().__init__(login_email, password, profile_photo_file_path)

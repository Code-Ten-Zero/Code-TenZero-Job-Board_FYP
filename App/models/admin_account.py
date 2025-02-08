from App.database import db
from .base_user_account import BaseUserAccount


class AdminAccount(BaseUserAccount):
    __tablename__ = "admin_accounts"
    
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, email: str, password: str) -> None:
        super().__init__(email, password)

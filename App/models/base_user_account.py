from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.declarative import declared_attr
from App.database import db


class BaseUserAccount(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    login_email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(120), nullable=False)
    profile_photo_file_path = db.Column(db.String, default=None)

    # @declared_attr
    # def notifications(cls):
    #     return db.relationship(
    #         'Notification', back_populates='user', lazy="dynamic", cascade="all, delete-orphan"
    #     )

    @declared_attr
    def type(cls):
        return db.Column(db.String(50))

    @declared_attr
    def __mapper_args__(cls):
        return {
            'polymorphic_identity': 'user',
            'polymorphic_on': cls.type
        }

    def __init__(self, login_email: str, password: str, profile_photo_file_path: str = None) -> None:
        self.login_email = login_email
        self.set_password(password)
        self.profile_photo_file_path = profile_photo_file_path

    def __str__(self) -> str:
        return f"""{self.__class__.__name__} Info:
    - ID: {self.id}
    - Email: {self.login_email}
    - Password Hash: [HIDDEN]
    - Profile Photo File Path: {self.profile_photo_file_path if self.profile_photo_file_path else "N/A"}
    """

    def __repr__(self) -> str:
        return (f"<{self.__class__.__name__} (id={self.id}, login_email='{self.login_email}', password_hash='[HIDDEN]', "
                f"profile_photo_file_path='{self.profile_photo_file_path if self.profile_photo_file_path else 'N/A'}')>")

    def __json__(self) -> dict:
        return {
            'id': self.id,
            'login_email': self.login_email,
            'password_hash': "[HIDDEN]",
            'profile_photo_file_path': self.profile_photo_file_path if self.profile_photo_file_path else None
        }

    @property
    def password(self) -> None:
        raise AttributeError(
            "Password is not accessible directly. Use set_password() or check_password() instead."
        )

    @password.setter
    def password(self, password: str) -> None:
        self.set_password(password)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

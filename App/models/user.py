from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique = True)
    password = db.Column(db.String(120), nullable=False)

#     __mapper_args__ = {
#       'polymorphic_identity': 'user',
#       'polymorphic_on': type
#   }

    def __init__(self, password, email):
        self.set_password(password)
        self.email = email

    def get_json(self):
        return{
            'id': self.id,
            'email': self.email
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


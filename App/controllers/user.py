from App.models import User, Admin, Alumni, Company
from App.database import db

# from sqlalchemy.orm import with_polymorphic

def create_user(password, email):
    newuser = User(password=password, email=email)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return db.session.query(Admin).all() + db.session.query(Alumni).all() + db.session.query(Company).all()
    # return User.query.all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, email):
    user = get_user(id)
    if user:
        user.email = email
        db.session.add(user)
        return db.session.commit()
    return None
    from App.models import User, Admin, Alumni, Company
from App.database import db

def get_user_by_email(email):
    user = None
    alumni = Alumni.query.filter_by(email=email).first()
    if alumni:
        user = alumni
        return user
    admin = Admin.query.filter_by(email=email).first()
    if admin:
        user = admin
        return user
    company = Company.query.filter_by(email=email).first()
    if company:
        user = company
        return user
    
    return user

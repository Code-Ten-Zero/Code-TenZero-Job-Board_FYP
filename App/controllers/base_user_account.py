from App.models import BaseUserAccount, AdminAccount, AlumnusAccount, CompanyAccount
from App.database import db

# from sqlalchemy.orm import with_polymorphic

# def create_user(password, login_email):
#     newuser = BaseUserAccount(password=password, login_email=login_email)
#     db.session.add(newuser)
#     db.session.commit()
#     return newuser

def get_user_by_email(login_email):
    # return User.query.filter_by(username=username).first()
    user = None
    #user = BaseUserAccount.query.filter_by(login_email=login_email).first()
    alumni = AlumnusAccount.query.filter_by(login_email=login_email).first()
    #alumni = AlumnusAccount.query.first()

    if alumni:
        print("got alumni by email")
        return alumni

    admin = AdminAccount.query.filter_by(login_email=login_email).first()
    if admin:
        print("got Admin by email")
        return admin

    company = CompanyAccount.query.filter_by(login_email=login_email).first()
    if company:
        print("got company by email")
        return company

    print("found nothing by email")
    return user

# def get_user_by_username(username):
#     # Define the polymorphic loading to include all subclasses of User
#     polymorphic_query = with_polymorphic(User, [User, Admin, Alumni, Company])

#     # Query using the polymorphic loading and filter by username
#     user = polymorphic_query.query.filter_by(username=username).first()
    
#     return user

# def get_user_by_username(username):
#     # Debugging: Print the generated SQL query
#     print(User.query.filter_by(username=username).first().statement)
    
#     # Attempt to retrieve the user by username
#     return User.query.filter_by(username=username).first()

def get_user(id):
    return BaseUserAccount.query.get(id)

def get_all_users():
    return db.session.query(AdminAccount).all() + db.session.query(AlumnusAccount).all() + db.session.query(CompanyAccount).all()
    # return User.query.all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.__json__() for user in users]
    return users

def update_user(id, login_email):
    user = get_user(id)
    if user:
        user.login_email = login_email
        db.session.add(user)
        return db.session.commit()
    return None
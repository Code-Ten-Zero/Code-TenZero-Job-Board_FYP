from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    jwt_required,
    JWTManager,
    get_jwt_identity,
    verify_jwt_in_request
)

from App.models import BaseUserAccount, AdminAccount, AlumnusAccount, CompanyAccount
from App.controllers import get_user_by_email


def login(login_email, password):
    user = get_user_by_email(login_email)

    if user and user.check_password(password):
        token = create_access_token(identity=login_email)
        response = jsonify(access_token=token)
        set_access_cookies(response, token)
        return response
    return None


def setup_jwt(app):
    jwt = JWTManager(app)

    # configure's flask jwt to resolve get_current_identity() to the corresponding user's ID
    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        for model in [AdminAccount, AlumnusAccount, CompanyAccount]:
            user = model.query.filter_by(login_email=identity).one_or_none()
            if user:
                return user.login_email
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        for model in [AdminAccount, AlumnusAccount, CompanyAccount]:
            user = model.query.filter_by(login_email=identity).one_or_none()
            if user:
                return user
        return None

    return jwt


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request()
            login_email = get_jwt_identity()
            current_user = get_user_by_email(login_email)
            is_authenticated = True
        except Exception as e:
            print(e)
            is_authenticated = False
            current_user = None
        return dict(is_authenticated=is_authenticated, current_user=current_user)

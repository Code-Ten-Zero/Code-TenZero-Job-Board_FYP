from flask import Blueprint, render_template, jsonify, request, flash, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from App.database import db

from App.controllers.auth import login
from App.controllers.base_user_account import get_all_users
from App.controllers.alumnus_account import add_alumnus_account, update_alumnus_account
from App.controllers.company_account import add_company_account

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

INDEX_PAGE_ROUTE = 'index_views.index_page'
LOGIN_PAGE_ROUTE = 'auth_views.login_page'

'''
Page/Action Routes
'''

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)


@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template(
        'message.html',
        title="Identify",
        message=f"You are logged in as {current_user.id} - {current_user.login_email}"
    )


@auth_views.route('/', methods=['GET'])
@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('homepage.html')


@auth_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('homepage.html')


@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    response = redirect(request.referrer)

    token_response = login(data['login_email'], data['password'])

    if token_response:
        token = token_response.json.get('access_token')
        response = redirect(url_for(INDEX_PAGE_ROUTE))
        set_access_cookies(response, token)
        flash('Logged in successfully.', 'success')
    else:
        flash('Invalid email or password', 'unsuccessful'), 401

    return response


@auth_views.route('/alumnus-signup', methods=['POST'])
def alumnus_signup_action():
    data = request.form
    response = None

    try:
        add_alumnus_account(
            data['login_email'],
            data['password'],
            data['first_name'],
            data['last_name'],
            data['phone_number']
        )

        token_response = login(data['login_email'], data['password'])
        token = token_response.json.get("access_token")

        response = redirect(url_for(INDEX_PAGE_ROUTE))
        set_access_cookies(response, token)
        flash('Account created!', 'success')

    except Exception:
        db.session.rollback()
        flash("Could not complete signup. Please try again.", 'unsuccessful')
        response = redirect(url_for(LOGIN_PAGE_ROUTE))

    return response


@auth_views.route('/company-signup', methods=['POST'])
def company_signup_action():
    data = request.form
    response = None

    try:
        add_company_account(
            data['login_email'],
            data['password'],
            data['registered_name'],
            data['mailing_address'],
            data['public_email'],
            data['website_url'],
            data['phone_number']
        )

        token_response = login(data['login_email'], data['password'])
        token = token_response.json.get("access_token")

        response = redirect(url_for(INDEX_PAGE_ROUTE))
        set_access_cookies(response, token)
        flash('Account created!', 'success')

    except Exception:
        db.session.rollback()
        flash("Could not complete signup. Please try again.", 'unsuccessful')
        response = redirect(url_for(LOGIN_PAGE_ROUTE))

    return response


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for(LOGIN_PAGE_ROUTE))
    flash("Logged Out!", 'success')
    unset_jwt_cookies(response)
    return response


'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    print("Incoming JSON data:", data)
    response = login(data['login_email'], data['password'])

    if not response:
        return jsonify(message='bad email or password given'), 401

    return response


@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"Login Email: {current_user.login_email}, id : {current_user.id}"})


@auth_views.route('/api/update_alumni', methods=['PUT'])
@jwt_required()
def update_user():
    data = request.json
    print("Incoming JSON PUT data:", data)
    # current_user.first_name = data.get('fname')
    # current_user.last_name = data.get('lname')
    # return jsonify({'message': f"First Name: {current_user.first_name}, Last Name : {current_user.last_name}"})

    my_alumni = update_alumnus_account(
        1, data.get('fname') , data.get('lname'),
        "",
        "",
        data.get('current_password'),
        "",
       "" )
    return jsonify({'message': f"First Name: {my_alumni.first_name}, Last Name : {my_alumni.last_name}"})


@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response

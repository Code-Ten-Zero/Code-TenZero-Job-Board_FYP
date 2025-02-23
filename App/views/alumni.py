from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
# from App.controllers import create_user

from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from .index import index_views


from App.controllers import(
    get_user_by_email,
    is_alumni_subscribed,
    subscribe,
    unsubscribe,
    set_alumni_modal_seen,
    update_alumni_info,
    get_listing
)

from App.models import(
    AlumnusAccount,
    CompanyAccount,
    AdminAccount
)

alumni_views = Blueprint('alumni_views', __name__, template_folder='../templates')

@alumni_views.route('/update_alumni/<id>', methods=['POST'])
@jwt_required()
def update_alumni(id):
    data = request.form
    first_name = data['fname']
    last_name = data['lname']
    phone_number = data['contact']
    login_email = data['email']

    current_password = data['current_password']
    confirm_current_password = data['confirm_current_password']
    new_password = data['new_password']
    confirm_new_password = data['confirm_new_password']

    if current_password != confirm_current_password:
        return {"message": "Current passwords do not match"}, 400

    if new_password and new_password != confirm_new_password:
            return {"message": "New passwords do not match"}, 400

    update_status = update_alumni_info(id, first_name, last_name, phone_number, login_email, current_password, new_password)

    if update_status:
        return {"message": "Alumni information updated successfully"}, 200
    else:
        return {"message": "Update failed. Check your information and try again."}, 400

@alumni_views.route('/view_my_account/<id>', methods=["GET"])
@jwt_required()
def view_my_account_page(id):
    user = get_user_by_email(current_user.login_email)
    try:
        return render_template('my-account-alumni.html', user=user)

    except Exception:
        flash('Error retreiving User')
        response = redirect(url_for('index_views.index_page'))

    return response

@alumni_views.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe_action():
    # get form data
    data = request.form
    response = None

    # print(data)
    # print([data['category']])
    # print(current_user.alumni_id)

    try:
        alumni = subscribe(current_user.id, data['category'])
        set_alumni_modal_seen(alumni.id)
        # print(alumni.get_json())
        response = redirect(url_for('index_views.index_page'))
        flash('Subscribed!', 'success')

    except Exception:
        # db.session.rollback()
        flash('Error subscribing', 'unsuccessful')
        response = redirect(url_for('auth_views.login_page'))

    return response

@alumni_views.route('/unsubscribe', methods=['POST'])
@jwt_required()
def unsubscribe_action():
    # get form data
    # data = request.form
    response = None

    # print(data)

    try:
        alumni = unsubscribe(current_user.id)
        # print(alumni.get_json())
        response = redirect(url_for('index_views.index_page'))
        flash('Unsubscribed!', 'success')

    except Exception:
        # db.session.rollback()
        flash('Error unsubscribing', 'unsuccessful')
        response = redirect(url_for('auth_views.login_page'))

    return response

# for unsubscribe route
# get the user and their categories with user.get_categories
# then call unsubscrive_action with user and their categores?

@alumni_views.route('/update_modal_seen', methods=['POST'])
@jwt_required()
def update_modal_seen():
    try:
        alumni = current_user  
        set_alumni_modal_seen(alumni.id)  
        db.session.commit() 
        return jsonify(message="Modal seen status updated successfully"), 200
        
    except Exception as e:
        db.session.rollback()  
        return jsonify(message="Error updating modal status"), 500
    
@alumni_views.route('/view_listing_alumni/<id>', methods=["GET"])
@jwt_required()
def view_listing_page(id):
    listing=get_listing(id)
    try:
        return render_template('view-listing-alumni.html', listing=listing)

    except Exception:
        flash('Error retreiving Listing')
        response = redirect(url_for('auth_views.login_page'))

    return response
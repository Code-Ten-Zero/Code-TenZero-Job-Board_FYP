from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
# from App.controllers import create_user

from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from .index import index_views


from App.controllers import(
    get_user_by_email,
    get_all_listings,
    get_company_listings,
    add_listing,
    add_categories,
    get_listing,
    set_request
)

from App.models import(
    AlumnusAccount,
    CompanyAccount,
    AdminAccount
)

company_views = Blueprint('company_views', __name__, template_folder='../templates')

@company_views.route('/view_applications/<int:job_id>', methods=['GET'])
@jwt_required()
def view_applications_page(job_id):

    # get the listing
    listing = get_listing(job_id)

    # applicants = listing.get_applicants()

    response = None
    print(listing)

    try:
        applicants = listing.get_applicants()
        print(applicants)
        return render_template('viewapp-company.html', applicants=applicants)

    except Exception:
        flash('Error receiving applicants', 'unsuccessful')
        response = redirect(url_for('index_views.index_page'))

    return response

@company_views.route('/add_listing', methods=['GET'])
@jwt_required()
def add_listing_page():
    # username = get_jwt_identity()
    # user = get_user_by_username(username)

    return render_template('companyform.html')

@company_views.route('/add_listing', methods=['POST'])
@jwt_required()
def add_listing_action():
    # username = get_jwt_identity()
    # user = get_user_by_username(username)
    data = request.form

    response = None

    # print(data)
    # print(current_user.company_name)

    try:
        #is_remote = False

        if 'is_remote' in data and data['is_remote'] == 'Yes':
            is_remote = True

        listing = add_listing(current_user.id, data['title'], data['position_type'],data['description'], data['monthly_salary_ttd'],
                              is_remote, data['job_site_address'], data['datetime_created'], data['datetime_last_modified'], admin_approval_status='PENDING')
        # print(listing)
        flash('Created job listing', 'success')
        response = redirect(url_for('index_views.index_page'))
    except Exception:
        flash('Error creating listing', 'unsuccessful')
        response = redirect(url_for('company_views.add_listing_page'))
    
    return response

@company_views.route('/request_delete_listing/<int:job_id>', methods=['GET'])
@jwt_required()
def request_delete_listing_action(job_id):

    listing = set_request(job_id, 'Delete')
    response = None

    if listing is not None:
        flash('Request for deletion sent!', 'success')
        response = redirect(url_for('index_views.index_page'))
    else:
        flash('Error sending request', 'unsuccessful')
        response = redirect(url_for('index_views.login_page'))

    return response

# @company_views.route('/request_edit_listing/<int:job_id>', methods=['GET'])
# @jwt_required()
# def request_edit_listing_action(job_id):

#     listing = set_request(job_id, 'Edit')
#     response = None
#     print(listing.request)

#     if listing is not None:
#         flash('Request for edit sent!', 'success')
#         response = redirect(url_for('index_views.index_page'))
#     else:
#         flash('Error sending request', 'unsuccessful')
#         response = redirect(url_for('index_views.login_page'))

#     return response

@company_views.route('/notifications', methods=['GET'])
@jwt_required()
def view_notifications_page():
    # Assuming current_user is the logged-in company
    if not isinstance(current_user, CompanyAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    try:
        # Fetch notifications for the company
        notifications = current_user.notifications  # Assuming the Company model has a notifications relationship
        return render_template('company_notifications.html', notifications=notifications, company=current_user)
    except Exception as e:
        flash('Error retrieving notifications', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))
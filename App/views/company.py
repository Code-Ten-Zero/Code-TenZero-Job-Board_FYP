from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
# from App.controllers import create_user
from datetime import date, datetime
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
    return render_template('companyform.html')

@company_views.route('/add_listing', methods=['POST'])
@jwt_required()
def add_listing_action():
    data = request.form
    response = None

    try:
        is_remote = False  # Default value
    
        if data.get('is_remote') == 'Yes':  # Check if the checkbox is checked
            is_remote = True
        
        job_site_address = "N/A" if is_remote else data.get('job_site_address', "(Not specified)")
      
        listing = add_listing(
            current_user.id,
            data['title'],
            data['position_type'],
            data['description'],
            data['monthly_salary_ttd'],
            is_remote,  # Pass correct is_remote value
            job_site_address,
            datetime_created=datetime.utcnow(),
            datetime_last_modified=datetime.utcnow(),
            admin_approval_status='PENDING'
        )

        flash('Created job listing', 'success')  # Fixed indentation
        response = redirect(url_for('index_views.index_page'))
    
    except Exception as e:
        flash(f'Error creating listing: {str(e)}', 'unsuccessful')  # Added error message for debugging
        response = redirect(url_for('index_views.index_page'))
    
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
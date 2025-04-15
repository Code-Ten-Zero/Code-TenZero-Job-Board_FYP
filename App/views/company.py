from flask import Blueprint, flash, redirect, render_template, request, url_for
from App.controllers.base_user_account import get_user_by_email
from App.models import db
from datetime import date, datetime
from flask_jwt_extended import current_user, jwt_required

from App.controllers.job_applications import get_job_applications_by_job_listing_id
from App.controllers.job_listing import (
    add_job_listing,
    get_job_listing,
)
from App.controllers.notifications import (
    notify_admins,
    notify_company_account,
    notify_subscribed_alumni
)
from App.models import (
    CompanyAccount
)

company_views = Blueprint(
    'company_views',
    __name__,
    template_folder='../templates'
)

"""
====== COMPANY ACCOUNT INFO ======
"""

@company_views.route('/view_company_account/<id>', methods=["GET"])
@jwt_required()
def view_my_account_page(id):
    user = get_user_by_email(current_user.login_email)
    try:
        return render_template('my-account-company.html', user=user)

    except Exception:
        flash('Error retreiving User')
        return redirect(url_for('index_views.index_page'))

"""
====== COMPANY JOB LISTINGS ======
"""

@company_views.route('/add_listing', methods=['GET'])
@jwt_required()
def add_listing_page():
    return render_template('companyform.html', user=current_user)


@company_views.route('/add_listing', methods=['POST'])
@jwt_required()
def add_listing_action():
    data = request.form
    response = None

    try:
        is_remote = False  # Default value

        if data.get('is_remote') == 'Yes':  # Check if the checkbox is checked
            is_remote = True

        job_site_address = "N/A" if is_remote else data.get(
            'job_site_address', "(Not specified)")

        add_job_listing(
            current_user.id,
            data['title'],
            data['position_type'],
            data['description'],
            int(data['monthly_salary_ttd']),
            is_remote,  # Pass correct is_remote value
            job_site_address
        )

        flash('Created job listing', 'success')  # Fixed indentation
        response = redirect(url_for('index_views.index_page'))

    except Exception as e:
        # Added error message for debugging
        flash(f'Error creating listing: {str(e)}', 'unsuccessful')
        response = redirect(url_for('index_views.index_page'))

    return response


@company_views.route('/request_delete_listing/<int:job_id>', methods=['GET'])
@jwt_required()
def request_delete_listing_action(job_id):

    listing = get_job_listing(job_id)

    if not listing:
        flash('Error sending request', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))
    
    try:
        listing.admin_approval_status = "REQUESTED DELETION"
        db.session.commit()
        notify_admins(
            f"{listing.company.registered_name} requested {listing.title} to be deleted"
        )
        flash('Request for deletion sent!', 'success')
        return redirect(url_for('index_views.index_page'))
    
    except Exception as e:
        flash('Could not send deletion request.', 'unsuccessful')
        print(f"Error requesting listing deletion: {e}")
        return redirect(url_for('index_views.index_page'))


@company_views.route('/request_edit_listing/<int:job_id>', methods=['GET'])
@jwt_required()
def request_edit_listing_action(job_id):

    listing = get_job_listing(job_id)

    if not listing:
        flash('Error sending request', 'unsuccessful')
        return redirect(url_for('index_views.login_page'))
    
    listing.admin_approval_status = "REQUESTED UPDATE"
    db.session.commit()
    flash('Request for edit sent!', 'success')
    return redirect(url_for('index_views.index_page'))
        

@company_views.route('/view_applications/<int:id>', methods=['GET'])
@jwt_required()
def view_applications_page(id):

    # get the listing
    listing = get_job_listing(id)

    print(listing)

    try:
        applications = get_job_applications_by_job_listing_id(listing.id)
        print(applications)
        return render_template('viewapp-company.html', applications=applications)

    except Exception:
        flash('Error receiving applicants', 'unsuccessful')
        response = redirect(url_for('index_views.index_page'))
        return response


"""
====== COMPANY NOTIFICATIONS ======
"""

@company_views.route('/company_notifications', methods=['GET'])
@jwt_required()
def view_notifications_page():
    # Assuming current_user is the logged-in company
    if not isinstance(current_user, CompanyAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    try:
        # Fetch notifications for the company
        # Assuming the Company model has a notifications relationship
        notifications = current_user.notifications
        return render_template('company_notifications.html', notifications=notifications, company=current_user)

    except Exception as e:
        flash('Error retrieving notifications', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

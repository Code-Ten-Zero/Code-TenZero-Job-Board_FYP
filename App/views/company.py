import os
from flask import Blueprint, current_app, flash, make_response, redirect, render_template, request, url_for, jsonify
from App.controllers.base_user_account import get_user_by_email
from App.models import db
from datetime import date, datetime
from werkzeug.utils import secure_filename
from flask_jwt_extended import current_user, jwt_required, unset_jwt_cookies

from App.controllers.company_account import get_company_account, update_company_account
from App.controllers.job_applications import get_job_application, get_job_applications_by_job_listing_id
from App.controllers.job_listing import (
    add_job_listing,
    get_job_listing,
    update_job_listing,
)
from App.controllers.notifications import (
    notify_admins,
    notify_company_account,
    notify_subscribed_alumni
)
from App.models import (
    CompanyAccount
)
from App.models.job_application import JobApplication
from App.models.notification import Notification

company_views = Blueprint(
    'company_views',
    __name__,
    template_folder='../templates'
)

"""
====== COMPANY ACCOUNT INFO ======
"""

@company_views.route('/update_company/<id>', methods=['POST'])
@jwt_required()
def update_company(id):
    if not isinstance(current_user, CompanyAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    user = get_user_by_email(current_user.login_email)
    data = request.form
    registered_name = data['registered_name']
    phone_number = data['contact']
    login_email = data['email']

    current_password = data['current_password']
    confirm_current_password = data['confirm_current_password']
    new_password = data['new_password']
    confirm_new_password = data['confirm_new_password']
    
    if not current_password or not confirm_current_password:
        flash('Current password fields are required', 'unsuccessful')
        return redirect(url_for('company_views.view_my_account_page', id=id, user=user))

    if current_password != confirm_current_password:
        flash('Current passwords do not match', 'unsuccessful')
        return redirect(url_for('company_views.view_my_account_page', id=id, user=user))

    if new_password != confirm_new_password:
        flash('New passwords do not match', 'unsuccessful') 
        return redirect(url_for('company_views.view_my_account_page', id=id, user=user))

    original_email = current_user.login_email
    
    update_status = update_company_account(
        id,
        registered_name,
        phone_number,
        login_email,
        current_password,
        new_password
    )

    if update_status:
        if login_email != original_email or new_password:
            flash("Email or password updated successfully. Please log in again.", 'success')
            response = make_response(redirect(url_for('auth_views.login_page')))
            unset_jwt_cookies(response)
            return response
        else:
            flash("Company information updated successfully", 'success')
            return redirect(url_for('company_views.view_my_account_page', id=id))
    else:
        flash("Update failed. Check your information and try again.", 'unsuccessful')
        return redirect(url_for('company.view_my_account_page', id=id))


@company_views.route('/update_company_profile_photo/<int:id>', methods=['POST'])
@jwt_required()
def update_profile_photo(id):
    # Ensure the user is an companyAccount and matches the route ID
    if not isinstance(current_user, CompanyAccount) or current_user.id != id:
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    if 'profile_pic' not in request.files:
        flash('No file part in the form', 'unsuccessful')
        return redirect(url_for('company_views.view_my_account_page', id=id))

    file = request.files['profile_pic']

    if file.filename == '':
        flash('No file selected', 'unsuccessful')
        return redirect(url_for('company_views.view_my_account_page', id=id))

    if file:
        try:
            # Ensure secure filename
            filename = secure_filename(file.filename)

            # Build absolute path to save
            save_folder = os.path.join(current_app.root_path, 'static', 'profile-images')
            os.makedirs(save_folder, exist_ok=True)

            # Save file
            file_path = os.path.join(save_folder, filename)
            file.save(file_path)

            # Save relative path in DB (for use with url_for('static', filename=...))
            relative_path = f"profile-images/{filename}"

            # Update database
            company = get_company_account(id)
            company.profile_photo_file_path = relative_path
            db.session.commit()

            flash("Profile picture updated successfully!", "success")
        except Exception as e:
            flash(f"An error occurred while uploading the photo: {str(e)}", "unsuccessful")

    return redirect(url_for('company_views.view_my_account_page', id=id))


@company_views.route('/view_company_account/<id>', methods=["GET"])
@jwt_required()
def view_my_account_page(id):
    user = get_user_by_email(current_user.login_email)
    try:
        return render_template('my-account-company.html', user=user)

    except Exception:
        flash('Error retreiving User', 'unsuccessful')
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
def edit_listing_page(job_id):
    listing = get_job_listing(job_id)
    if not listing:
        flash('Error sending request', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))
    return render_template('company-edit-listing.html', user=current_user, listing=listing)

@company_views.route('/request_edit_listing/<int:job_id>', methods=['POST'])
@jwt_required()
def request_edit_listing_action(job_id):
    if not isinstance(current_user, CompanyAccount):  # Adjust to your actual user model
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    data = request.form
    title = data['title']
    position_type = data['position_type']
    description = data['description']
    monthly_salary_ttd = data['monthly_salary_ttd']
    is_remote = True if data.get('is_remote') == 'Yes' else False
    job_site_address = data['job_site_address'] if not is_remote else None

    update_status = update_job_listing(
        job_id,
        title,
        position_type,
        description,
        monthly_salary_ttd,
        is_remote,
        job_site_address
    )
    
    if update_status:
        update_status.admin_approval_status='REQUESTED UPDATE'
        db.session.commit()
        flash("Edit request submitted successfully", 'success')
    else:
        flash("Failed to request update. Please try again.", 'unsuccessful')

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

"""
====== COMPANY APPLICATION HANDLING ======
"""
 
    
@company_views.route('/application_status_update/<int:id>', methods=['POST'])
@jwt_required()   
def update_status(id):
    new_status = request.form.get('status')
    
    application = JobApplication.query.filter_by(id=id).first()
    
    if not application:
        flash("Application not found.", "unsuccessful")
        return redirect(url_for('index_views.index_page'))
    
    try:
        application.company_approval_status = new_status
        db.session.commit()

        flash(
            f"Status updated to '{new_status.capitalize()}' for "
            f"{application.alumnus.first_name} {application.alumnus.last_name}.", 
            "success"
        )

        # Create notification message
        notification_message = (
            f"Hello there {application.alumnus.first_name}, your application status for "
            f"'{application.job_listing.title}' has changed to '{new_status.capitalize()}'."
        )

        new_notification = Notification(
            alumnus_id=application.alumnus_id,
            company_id=None,
            admin_id=None,
            message=notification_message
        )

        db.session.add(new_notification)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash("Error updating status. Please try again.", "unsuccessful")

    return redirect(url_for('company_views.view_applications_page', id=application.job_listing_id))




@company_views.route('/api/add_listing', methods=['POST'])
@jwt_required()
def api_add_listing_action():
    data = request.json
    print("Incoming JSON PUT data:", data)
    response = None

    try:
        is_remote = data.get('is_remote')
        if is_remote == "True" :
            is_remote = True
        else:
            is_remote = False
        job_site_address = data.get('job_site_address')
        add_job_listing(
            current_user.id,
            data['title'],
            data['position_type'],
            data['description'],
            data['monthly_salary_ttd'],
            is_remote,
            job_site_address
        )
        return jsonify({"message": "Job listing added successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@company_views.route('/api/request_delete_listing/<int:job_id>', methods=['GET'])
@jwt_required()
def api_request_delete_listing_action(job_id):

    listing = get_job_listing(job_id)
    
    try:
        listing.admin_approval_status = "REQUESTED DELETION"
        db.session.commit()
        notify_admins(
            f"{listing.company.registered_name} requested {listing.title} to be deleted"
        )
        return jsonify({"message": "Job listing requested for deletion"}), 200
    
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
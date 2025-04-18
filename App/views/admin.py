import os
from flask import Blueprint, current_app, flash, make_response, redirect, render_template, request, url_for, jsonify
from flask_jwt_extended import current_user, jwt_required, unset_jwt_cookies
from App.models import db, JobListing, AdminAccount
from werkzeug.utils import secure_filename


from App.controllers.admin_account import get_admin_account, update_admin_account
from App.controllers.base_user_account import get_user_by_email
from App.controllers.job_listing import (
    approve_job_listing,
    unapprove_job_listing,
    delete_job_listing
)

from App.controllers.alumnus_account import get_alumnus_account
from App.controllers.company_account import get_company_account
from App.controllers.company_subscription import get_company_subscriptions_by_company_id
from App.controllers.job_listing import (
    get_job_listing,
    delete_job_listing
)
from App.controllers.notifications import (
    mark_notification_as_reviewed,
    notify_company_account,
    notify_subscribed_alumni
)

from App.models.notification import Notification
from App.utils.email import (
    send_job_published_email,
    send_job_unpublished_email,
    send_job_deleted_email
)

admin_views = Blueprint(
    'admin_views',
    __name__,
    template_folder='../templates'
)

INDEX_PAGE_ROUTE = 'index_views.index_page'

"""
====== JOB ACTION ROUTES ======
"""

@admin_views.route('/publish_job/<int:job_id>', methods=['POST'])
@jwt_required()
def publish_job(job_id):
    """
    Sets a job listing's status to "APPROVED" and notifies the associated company and subscribed alumni.
    """
    if not isinstance(current_user, AdminAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for(INDEX_PAGE_ROUTE))

    approved_listing = approve_job_listing(job_id)

    if not approved_listing:
        flash('Job not found or could not be published.', 'unsuccessful')
        return redirect(url_for(INDEX_PAGE_ROUTE))

    company = get_company_account(approved_listing.company_id)

    notify_company_account(
        f"Your job listing, {approved_listing.title} has been published!",
        company.id
    )
    send_job_published_email(company, approved_listing, company)

    notify_subscribed_alumni(
        f"{company.registered_name} posted a new listing, {approved_listing.title}!",
        company.id
    )
    for subscription in get_company_subscriptions_by_company_id(company.id):
        alumnus_obj = get_alumnus_account(subscription.alumnus_id)
        send_job_published_email(
            alumnus_obj,
            approved_listing,
            company
        )

    flash('Job published successfully!', 'success')
    return redirect(url_for(INDEX_PAGE_ROUTE))


@admin_views.route('/unpublish_job/<int:job_id>', methods=['POST'])
@jwt_required()
def unpublish_job(job_id):
    """
    Sets a job listing's status to "PENDING" and notifies the associated company and subscribed alumni.
    """
    if not isinstance(current_user, AdminAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for(INDEX_PAGE_ROUTE))

    unapproved_listing = unapprove_job_listing(job_id)

    if not unapproved_listing:
        flash('Job not found or unpublishing failed.', 'unsuccessful')
        return redirect(url_for(INDEX_PAGE_ROUTE))

    company = get_company_account(unapproved_listing.company_id)

    notify_company_account(
        f"Your job listing, {unapproved_listing.title} has been temporarily unpublished!",
        company.id
    )
    send_job_unpublished_email(
        company,
        unapproved_listing,
        company
    )

    notify_subscribed_alumni(
        f"The job listing {unapproved_listing.title} by company {company.registered_name} has been temporarily unpublished.",
        company.id
    )
    for subscription in get_company_subscriptions_by_company_id(company.id):
        alumnus_obj = get_alumnus_account(subscription.alumnus_id)
        send_job_unpublished_email(
            alumnus_obj,
            unapproved_listing,
            company
        )

    flash('Job unpublished successfully!', 'success')
    return redirect(url_for(INDEX_PAGE_ROUTE))


@admin_views.route('/delete_listing/<int:job_id>', methods=['POST'])
@jwt_required()
def delete_listing_action(job_id):
    """
    Deletes a job listing and notifies the associated company and subscribed alumni.
    """
    if not isinstance(current_user, AdminAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for(INDEX_PAGE_ROUTE))

    # Store a temp. copy of the listing to populate deletion message
    temp_listing_copy = get_job_listing(job_id)

    if not temp_listing_copy:
        flash('Job listing not found.', 'unsuccessful')
        return redirect(url_for(INDEX_PAGE_ROUTE))

    if not delete_job_listing(job_id,current_user.id):
        flash('Error deleting job listing', 'unsuccessful')

    else:
        company = get_company_account(temp_listing_copy.company_id)

        notify_company_account(
            f"Your job listing, {temp_listing_copy.title} has been deleted!",
            company.id
        )
        send_job_deleted_email(company, temp_listing_copy, company)

        notify_subscribed_alumni(
            f"{company.registered_name}'s listing, {temp_listing_copy.title} has been deleted!",
            company.id
        )
        for subscription in get_company_subscriptions_by_company_id(company.id):
            alumnus_obj = get_alumnus_account(subscription.alumnus_id)
            send_job_deleted_email(
                alumnus_obj,
                temp_listing_copy,
                company
            )

        flash('Job listing deleted!', 'success')

    return redirect(url_for(INDEX_PAGE_ROUTE))

"""
====== ADMIN ACCOUNT INFO ======
"""

@admin_views.route('/update_admin/<id>', methods=['POST'])
@jwt_required()
def update_alumnus(id):
    if not isinstance(current_user, AdminAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    user = get_user_by_email(current_user.login_email)
    data = request.form
    login_email = data['email']

    current_password = data['current_password']
    confirm_current_password = data['confirm_current_password']
    new_password = data['new_password']
    confirm_new_password = data['confirm_new_password']

    if not current_password or not confirm_current_password:
        flash('Current password fields are required', 'unsuccessful')
        return redirect(url_for('admin_views.view_my_account_page', id=id, user=user))
    
    if current_password != confirm_current_password:
        flash('Current passwords do not match', 'unsuccessful')
        return redirect(url_for('admin_views.view_my_account_page', id=id, user=user))

    if new_password != confirm_new_password:
        flash('New passwords do not match', 'unsuccessful') 
        return redirect(url_for('admin_views.view_my_account_page', id=id, user=user))
    original_email = current_user.login_email
    
    update_status = update_admin_account(
        id,
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
        flash("Update failed. Check your information and try again.", 'unsuccessful')
        return redirect(url_for('admin_views.view_my_account_page', id=id))


@admin_views.route('/update_admin_profile_photo/<int:id>', methods=['POST'])
@jwt_required()
def update_profile_photo(id):
    # Ensure the user is an AlumnusAccount and matches the route ID
    if not isinstance(current_user, AdminAccount) or current_user.id != id:
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    if 'profile_pic' not in request.files:
        flash('No file part in the form', 'unsuccessful')
        return redirect(url_for('admin_views.view_my_account_page', id=id))

    file = request.files['profile_pic']

    if file.filename == '':
        flash('No file selected', 'unsuccessful')
        return redirect(url_for('admin_views.view_my_account_page', id=id))

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
            admin = get_admin_account(id)
            admin.profile_photo_file_path = relative_path
            db.session.commit()

            flash("Profile picture updated successfully!", "success")
        except Exception as e:
            flash(f"An error occurred while uploading the photo: {str(e)}", "unsuccessful")

    return redirect(url_for('admin_views.view_my_account_page', id=id))


@admin_views.route('/view_admin_account/<id>', methods=["GET"])
@jwt_required()
def view_my_account_page(id):
    #Retrieve the current user and display the admin page
    user = get_user_by_email(current_user.login_email)
    try:
        return render_template('my-account-admin.html', user=user)

    except Exception:
        flash('Error retreiving User')
        return redirect(url_for('index_views.index_page'))


"""
====== ADMIN NOTIFICATIONS ======
"""


@admin_views.route('/admin_notifications', methods=['GET'])
@jwt_required()
def view_notifications_page():
    """
    Displays notifications for the currently logged-in admin.
    """
    if not isinstance(current_user, AdminAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for(INDEX_PAGE_ROUTE))

    try:
        # Fetch notifications for the alumnus
        notifications = current_user.notifications.filter_by(reviewed_by_user=False).all()
        return render_template('admin_notifications.html', notifications=notifications, admin=current_user)

    except Exception as e:
        print(f"[ERROR] Failed to retrieve admin notifications: {e}")
        flash('Error retrieving notifications.', 'unsuccessful')
        return redirect(url_for(INDEX_PAGE_ROUTE))

@admin_views.route('/update/admin/notification_status/<int:notification_id>', methods=['POST'])
@jwt_required()
def notification_status(notification_id):
    notification = Notification.query.get(notification_id)
    #Once notification is found, mark as read
    if notification:
        mark_notification_as_reviewed(notification_id)
        return jsonify({'success': True}), 200

    return jsonify({'success': False, 'message': 'Notification not found'}), 404

@admin_views.route('/check_admin_unread_notifications', methods=['GET'])
@jwt_required()
def check_notifications():
    if not isinstance(current_user, AdminAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    # Fetch unread notifications for the current user
    unread_notifications = Notification.query.filter_by(
    admin_id=current_user.id, reviewed_by_user=False).all()

    # Determine if there are new notifications
    has_new_notifications = len(unread_notifications) > 0
    return jsonify({'has_new_notifications': has_new_notifications})

"""
====== API TESTING ======
"""

@admin_views.route('/api/delete_listing/<int:job_id>', methods=['DELETE'])
@jwt_required()
def api_delete_listing(job_id):
    job = JobListing.query.get(job_id)

    if not job:
        return jsonify({'error': 'Job listing not found'}), 404
    
    try:
        db.session.delete(job)
        db.session.commit()
        return jsonify({'message': f'Job listing {job_id} deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete job listing', 'details': str(e)}), 500

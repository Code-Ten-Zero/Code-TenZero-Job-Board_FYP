import os
from flask import Blueprint, current_app, flash,  jsonify, redirect, render_template, request, url_for
from App.models import db
from werkzeug.utils import secure_filename

from flask_jwt_extended import current_user, jwt_required

from App.models import (
    AlumnusAccount,
    CompanyAccount,
    Notification,
    SavedJobListing,
    JobApplication
)

from App.controllers.alumnus_account import update_alumnus_account
from App.controllers.base_user_account import get_user_by_email
from App.controllers.company_subscription import (
    add_company_subscription,
    get_company_subscription
)
from App.controllers.job_listing import get_job_listing
from App.controllers.saved_job_listing import get_saved_job_listings_by_alumnus_id


alumnus_views = Blueprint(
    'alumnus_views',
    __name__,
    template_folder='../templates'
)


@alumnus_views.route('/update_alumnus/<id>', methods=['POST'])
@jwt_required()
def update_alumnus(id):
    if not isinstance(current_user, AlumnusAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    user = get_user_by_email(current_user.login_email)
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
        flash("Current passwords do not match")
        return render_template('my-account-alumnus.html', user=user)

    if new_password != confirm_new_password:
        flash("New passwords do not match")
        return render_template('my-account-alumnus.html', user=user)

    update_status = update_alumnus_account(
        id,
        first_name,
        last_name,
        phone_number,
        login_email,
        current_password,
        new_password
    )

    if update_status:
        flash("Alumnus' information updated successfully")
    else:
        flash("Update failed. Check your information and try again.")

    return render_template('my-account-alumnus.html', user=user)


@alumnus_views.route('/view_my_account/<id>', methods=["GET"])
@jwt_required()
def view_my_account_page(id):
    user = get_user_by_email(current_user.login_email)
    try:
        return render_template('my-account-alumnus.html', user=user)

    except Exception:
        flash('Error retreiving User')
        return redirect(url_for('index_views.index_page'))


@alumnus_views.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe_action():
    """
    Allows an alumnus to subscribe to a company to receive updates about job listings.
    """
    if not isinstance(current_user, AlumnusAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    selected_companies = request.form.getlist('company')

    if not selected_companies:
        flash('No companies selected!', 'error')
    try:
        alumnus_id = current_user.id

        # Check if the alumnus and company exist in the database
        alumnus = AlumnusAccount.query.get(alumnus_id)
        companies = CompanyAccount.query.filter(
            CompanyAccount.registered_name.in_(selected_companies)).all()

        if not alumnus:
            flash('Alumnus not found!', 'error')
            return redirect(url_for('index_views.index_page'))

        if not companies:
            flash('No valid companies selected!', 'error')
            return redirect(url_for('index_views.index_page'))

        new_subscription_added = False

        for company in companies:
            # Check if the alumnus is already subscribed to the company
            existing_subscription = get_company_subscription(
                alumnus_id=alumnus.id, company_id=company.id)

            if existing_subscription:
                continue  # Skip if the alumnus is already subscribed to this company

            # Create a new subscription
            add_company_subscription(
                alumnus_id=alumnus.id, company_id=company.id)
            new_subscription_added = True  # Mark that a new subscription has been added

        db.session.commit()

        if new_subscription_added:
            flash('Successfully subscribed to selected companies!', 'success')
        else:
            flash('You are already subscribed to all selected companies!', 'warning')

        return redirect(url_for('index_views.index_page'))

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", 'unsuccessful')
        return redirect(url_for('index_views.index_page'))


# @alumnus_views.route('/update_modal_seen', methods=['POST'])
# @jwt_required()
# def update_modal_seen():
#     try:
#         alumnus = current_user
#         set_alumnus_modal_seen(alumnus.id)
#         db.session.commit()
#         return jsonify(message="Modal seen status updated successfully"), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify(message="Error updating modal status"), 500


@alumnus_views.route('/view_listing_alumnus/<id>', methods=["GET"])
@jwt_required()
def view_listing_page(id):
    listing = get_job_listing(id)
    saved_listings = get_saved_job_listings_by_alumnus_id(current_user.id)

    try:
        return render_template('view-listing-alumnus.html', listing=listing, saved_listings=saved_listings)

    except Exception:
        flash('Error retreiving Listing')
        response = redirect(url_for('index_views.index_page'))

    return response


@alumnus_views.route('/get_saved_listing', methods=['GET'])
@jwt_required()
def get_saved_job_listing():
    if not isinstance(current_user, AlumnusAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    already_saved = SavedJobListing.query.filter_by(
        alumnus_id=current_user.id).all()

    return jsonify([listing.job_listing_id for listing in already_saved])


@alumnus_views.route('/save_listing/<job_listing_id>', methods=['POST'])
@jwt_required()
def save_job_listing(job_listing_id):
    if not isinstance(current_user, AlumnusAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    alumnus_id = current_user.id

    already_saved = SavedJobListing.query.filter_by(
        alumnus_id=alumnus_id, job_listing_id=job_listing_id).first()

    if not already_saved:
        new_saved_job_listing = SavedJobListing(
            alumnus_id=alumnus_id, job_listing_id=job_listing_id)
        db.session.add(new_saved_job_listing)
        db.session.commit()

        return jsonify({"message": "Job saved successfully!", "status": "saved"}), 201


@alumnus_views.route('/remove_saved_listing/<job_listing_id>', methods=['GET'])
@jwt_required()
def remove_listing(job_listing_id):
    if not isinstance(current_user, AlumnusAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    already_saved_job = SavedJobListing.query.filter_by(
        alumnus_id=current_user.id, job_listing_id=job_listing_id).first()

    if not already_saved_job:
        return jsonify({"message": "Job not saved!", "status": "error"}), 404

    db.session.delete(already_saved_job)
    db.session.commit()

    return jsonify({"message": "Job Removed from saved listings", "status": "removed"}), 200


@alumnus_views.route('/apply_to_listing/<int:job_listing_id>', methods=['POST'])
@jwt_required()
def apply(job_listing_id):
    if not isinstance(current_user, AlumnusAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    # Get form data
    work_experience = request.form.get("work-experience")
    resume = request.files["resume"]

    # Secure and save filename
    filename = secure_filename(resume.filename)
    static_folder = os.path.join(current_app.root_path, 'static')
    resume_path = os.path.join(static_folder, 'uploads', 'resumes', filename)
    file_path = os.path.join('uploads', 'resumes', filename)

    # Save the file to the directory
    resume.save(resume_path)  # This actually writes the file!
    resume_path = resume_path.replace("\\", "/")
    file_path = file_path.replace("\\", "/")
    alumnus_id = current_user.id

    # Create a new JobApplication record
    new_application = JobApplication(
        alumnus_id=alumnus_id,
        job_listing_id=job_listing_id,
        resume_file_path=file_path,
        work_experience=work_experience,
    )

    # Save to the database
    db.session.add(new_application)
    db.session.commit()

    # print(new_application) for debugging purposes CTZ

    flash("Application submitted successfully!", "success")
    return redirect(url_for("index_views.index_page"))


@alumnus_views.route('/alumnus_notifications', methods=['GET'])
@jwt_required()
def view_notifications_page():
    if not isinstance(current_user, AlumnusAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    try:
        # Fetch notifications for the alumnus
        notifications = current_user.notifications.all()
        return render_template('alumnus_notifications.html', notifications=notifications, alumnus=current_user)

    except Exception as e:
        flash('Error retrieving notifications', 'unsuccessful')
        print(f'Error retrieving notifications: {e}')
        return redirect(url_for('index_views.index_page'))


@alumnus_views.route('/check_unread_notifications', methods=['GET'])
@jwt_required()
def check_notifications():
    if not isinstance(current_user, AlumnusAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    # Fetch unread notifications for the current user
    unread_notifications = Notification.query.filter_by(
        alumnus_id=current_user.id, reviewed_by_user=False).all()

    # Determine if there are new notifications
    has_new_notifications = len(unread_notifications) > 0
    return jsonify({'has_new_notifications': has_new_notifications})

import os
from flask import Blueprint, current_app, flash,  jsonify, make_response, redirect, render_template, request, url_for
from App.models import db
from werkzeug.utils import secure_filename

from flask_jwt_extended import current_user, jwt_required, unset_jwt_cookies

from App.models import (
    AlumnusAccount,
    CompanyAccount,
    Notification,
    SavedJobListing,
    JobApplication
)

from App.controllers.alumnus_account import get_alumnus_account, update_alumnus_account
from App.controllers.base_user_account import get_user_by_email
from App.controllers.company_subscription import (
    add_company_subscription,
    get_company_subscription
)
from App.controllers.job_listing import get_job_listing, get_job_listing_by_similar_description, get_job_listings_by_company_id, get_job_listings_by_exact_position_type, get_job_listings_by_salary_range, get_job_listings_by_similar_position_type, get_job_listings_by_similar_title
from App.controllers.saved_job_listing import get_saved_job_listings_by_alumnus_id
from App.controllers.company_account import get_company_account
from App.models.job_listing import JobListing

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

    user = get_alumnus_account(current_user.id)
    data = request.form
    first_name = data['fname']
    last_name = data['lname']
    phone_number = data['contact']
    login_email = data['email']

    current_password = data['current_password']
    confirm_current_password = data['confirm_current_password']
    new_password = data['new_password']
    confirm_new_password = data['confirm_new_password']
    
    if not current_password or not confirm_current_password:
        flash('Current password fields are required', 'unsuccessful')
        return redirect(url_for('alumnus_views.view_my_account_page', id=id, user=user))

    if current_password != confirm_current_password:
        flash('Current passwords do not match', 'unsuccessful')
        return redirect(url_for('alumnus_views.view_my_account_page', id=id, user=user))

    if new_password != confirm_new_password:
        flash('New passwords do not match', 'unsuccessful') 
        return redirect(url_for('alumnus_views.view_my_account_page', id=id, user=user))
    
    original_email = current_user.login_email
    
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
        if login_email != original_email or new_password:
            flash("Email or password updated successfully. Please log in again.", 'success')
            response = make_response(redirect(url_for('auth_views.login_page')))
            unset_jwt_cookies(response)
            return response
        else:
            flash("Alumnus' information updated successfully", 'success')
            return redirect(url_for('alumnus_views.view_my_account_page'))
    else:
        flash("Update failed. Check your information and try again.", 'unsuccessful')
        return redirect(url_for('alumnus_views.view_my_account_page', id=id))


@alumnus_views.route('/update_profile_photo/<int:id>', methods=['POST'])
@jwt_required()
def update_profile_photo(id):
    # Ensure the user is an AlumnusAccount and matches the route ID
    if not isinstance(current_user, AlumnusAccount) or current_user.id != id:
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    if 'profile_pic' not in request.files:
        flash('No file part in the form', 'unsuccessful')
        return redirect(url_for('alumnus_views.view_my_account_page', id=id))

    file = request.files['profile_pic']

    if file.filename == '':
        flash('No file selected', 'unsuccessful')
        return redirect(url_for('alumnus_views.view_my_account_page', id=id))

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
            alumnus = get_alumnus_account(id)
            alumnus.profile_photo_file_path = relative_path
            db.session.commit()

            flash("Profile picture updated successfully!", "success")
        except Exception as e:
            flash(f"An error occurred while uploading the photo: {str(e)}", "unsuccessful")

    return redirect(url_for('alumnus_views.view_my_account_page', id=id))

@alumnus_views.route('/view_my_account/<id>', methods=["GET"])
@jwt_required()
def view_my_account_page(id):
    user = get_alumnus_account(current_user.id)
    try:
        return render_template('my-account-alumnus.html', user=user)

    except Exception:
        flash('Error retreiving User', 'unsuccessful')
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
        flash('No companies selected!', 'unsuccessful')
    try:
        alumnus_id = current_user.id

        # Check if the alumnus and company exist in the database
        alumnus = AlumnusAccount.query.get(alumnus_id)
        companies = CompanyAccount.query.filter(
            CompanyAccount.registered_name.in_(selected_companies)).all()

        if not alumnus:
            flash('Alumnus not found!', 'unsuccessful')
            return redirect(url_for('index_views.index_page'))

        if not companies:
            flash('No valid companies selected!', 'unsuccessful')
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
    user=current_user
    listing = get_job_listing(id)
    saved_listings = get_saved_job_listings_by_alumnus_id(user.id)

    try:
        return render_template('view-listing-alumnus.html', listing=listing, saved_listings=saved_listings, user=user)

    except Exception:
        flash('Error retreiving Listing', 'unsuccessful')
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

    existing_application = JobApplication.query.filter_by(
    alumnus_id=current_user.id,
    job_listing_id=job_listing_id).first()
    
    if existing_application:
        flash("You have already applied to this job listing.", "unsuccessful")
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

@alumnus_views.route('/view_company_listings/<id>', methods=['GET'])
@jwt_required()
def view_company_listings(id):
    user=current_user
    company=get_company_account(id)
    company_listings = get_job_listings_by_company_id(id)
    approved_company_listings = [job for job in company_listings if job.admin_approval_status=="APPROVED"] 
    saved = get_saved_job_listings_by_alumnus_id(user.id)
    return render_template('alumnus-company-listings.html', user=user, company_listings=approved_company_listings, saved=saved, company=company)

@alumnus_views.route('/search_listings', methods=['GET'])
def search_jobs():
    search_term = request.args.get('search','')
    position_type = request.args.get('position')
    job_site_address = request.args.get('location')
    min_salary = request.args.get('min_salary', type=int)
    max_salary = request.args.get('max_salary', type=int)

    query = JobListing.query.filter_by(admin_approval_status='APPROVED')
    
    if search_term:
        search_term = search_term.strip()
        query = query.filter(
            (JobListing.title.ilike(f"%{search_term}%")) |
            (JobListing.company.has(CompanyAccount.registered_name.ilike(f"%{search_term}%")))
        )

    if position_type:
        query = query.filter_by(position_type=position_type)

    if job_site_address:
        query = query.filter_by(job_site_address=job_site_address)

    if min_salary is not None and max_salary is not None:
        query = query.filter(
            JobListing.monthly_salary_ttd >= min_salary,
            JobListing.monthly_salary_ttd <= max_salary
        )

    jobs = query.all()

    job_data = [ {
        'id': job.id,
        'title': job.title,
        'position_type': job.position_type,
        'job_site_address': job.job_site_address,
        'company_name': job.company.registered_name,
        'company_logo': url_for('static', filename=job.company.profile_photo_file_path)
    } for job in jobs ]

    return jsonify(job_data)  # Always return a list — even if it's empty, this is so user can get output messages when searches turn up empty

import os
from flask import Blueprint, app, current_app, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
from werkzeug.utils import secure_filename

from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from .index import index_views


from App.controllers import(
    get_user_by_email,
    is_alumni_subscribed,
    subscribe,
    unsubscribe,
    set_alumni_modal_seen,
    update_alumni_info,
    get_listing,
    get_all_listings,
    get_approved_listings,
    get_saved_listings
)

from App.models import(
    AlumnusAccount,
    CompanyAccount,
    AdminAccount,
    SavedJobListing,
    JobApplication,
    CompanySubscription
)

alumni_views = Blueprint('alumni_views', __name__, template_folder='../templates')

@alumni_views.route('/update_alumni/<id>', methods=['POST'])
@jwt_required()
def update_alumni(id):
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
        flash ("Current passwords do not match")
        return render_template('my-account-alumni.html', user=user)

    if new_password != confirm_new_password:
        flash ("New passwords do not match")
        return render_template('my-account-alumni.html', user=user)

    update_status = update_alumni_info(id, first_name, last_name, phone_number, login_email, current_password, new_password)

    if update_status:
        flash ("Alumni information updated successfully")
        return render_template('my-account-alumni.html', user=user)
    else:
        flash("Update failed. Check your information and try again.")
        return render_template('my-account-alumni.html', user=user)

    return render_template('my-account-alumni.html', user=user)

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
    # # get form data
    data = request.form
    response = None
    
    """
    Allows an alumnus to subscribe to a company to receive updates about job listings.
    """
    try:
        # Get the alumnus ID and company ID from the request
        alumnus_id = request.json.get('alumnus_id')
        company_id = request.json.get('company_id')
        
        # Check if the alumnus and company exist in the database
        alumnus = AlumnusAccount.query.get(alumnus_id)
        company = CompanyAccount.query.get(company_id)
        
        if not alumnus or not company:
            flash('Alumnus or Company not found.', 'error') 

        # Check if the subscription already exists
        existing_subscription = CompanySubscription.query.filter_by(
            alumnus_id=alumnus_id, company_id=company_id).first()
        
        if existing_subscription:
           flash('You are already subscribed.', 'error'), 409
        
        # Create a new subscription
        new_alumni_subscription = CompanySubscription(alumnus_id=alumnus_id, company_id=company_id)
        db.session.add(new_alumni_subscription)
        db.session.commit()

        # Flash a success message
        flash('Subscribed successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

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
    saved_listings=get_saved_listings(current_user.id)
    
    try:
        return render_template('view-listing-alumni.html', listing=listing, saved_listings=saved_listings)

    except Exception:
        flash('Error retreiving Listing')
        response = redirect(url_for('index_views.index_page'))

    return response


@alumni_views.route('/get_saved_listing', methods=['GET'])
@jwt_required()
def get_saved_job_listing():
    alumnus_id = current_user.id

    already_saved = SavedJobListing.query.filter_by(alumnus_id=alumnus_id).all()

    return jsonify([listing.job_listing_id for listing in already_saved])

@alumni_views.route('/save_listing/<job_id>', methods=['POST'])
@jwt_required()
def save_job_listing(job_id):
    alumnus_id = current_user.id

    already_saved = SavedJobListing.query.filter_by(alumnus_id=alumnus_id, job_listing_id=job_id).first()

    if not already_saved:
        new_saved_job_listing = SavedJobListing(alumnus_id=alumnus_id, job_listing_id=job_id)
        db.session.add(new_saved_job_listing)
        db.session.commit()

        return jsonify({"message": "Job saved successfully!", "status": "saved"}), 201

@alumni_views.route('/remove_saved_listing/<job_id>', methods=['GET'])
@jwt_required()
def remove_listing(job_id):
    alumnus_id = current_user.id

    already_saved_job = SavedJobListing.query.filter_by(alumnus_id=alumnus_id, job_listing_id=job_id).first()

    if not already_saved_job:
        return jsonify({"message": "Job not saved!", "status": "error"}), 404
    
    db.session.delete(already_saved_job)
    db.session.commit()

    return jsonify({"message": "Job Removed from saved listings", "status":"removed"}), 200

@alumni_views.route('/apply_to_listing/<int:job_id>', methods=['POST'])
@jwt_required()
def apply(job_id):
    # Get form data
    work_experience = request.form.get("work-experience")
    resume = request.files["resume"]

    # Secure and save filename
    filename = secure_filename(resume.filename)
    static_folder = os.path.join(current_app.root_path, 'static')
    resume_path = os.path.join(static_folder, 'uploads', 'resumes', filename)
    file_path =  os.path.join('uploads', 'resumes', filename)

    # Save the file to the directory
    resume.save(resume_path)  # This actually writes the file!
    resume_path = resume_path.replace("\\", "/")
    file_path = file_path.replace("\\", "/")
    alumnus_id = current_user.id

    # Create a new JobApplication record
    new_application = JobApplication(
        alumnus_id=alumnus_id,
        job_listing_id=job_id,
        resume_file_path=file_path,  
        work_experience=work_experience,
    )

    # Save to the database
    db.session.add(new_application)
    db.session.commit()

    # print(new_application) for debugging purposes CTZ

    flash("Application submitted successfully!", "success")
    return redirect(url_for("index_views.index_page"))

    



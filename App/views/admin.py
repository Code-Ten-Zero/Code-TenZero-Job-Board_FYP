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
    delete_listing,
    toggle_listing_approval,
    notify_subscribed_alumnus,
    notify_company_account
)

from App.models import(
    AlumnusAccount,
    CompanyAccount,
    AdminAccount,
    JobListing,
    Notification
)

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

# handle publish
@admin_views.route('/publish_job/<int:job_id>', methods=['POST'])
@jwt_required()
def publish_job(job_id):
    toggled = toggle_listing_approval(job_id,status='APPROVED') # Set the job as approved

    if toggled:
        
        job_listing = JobListing.query.get(job_id)
        if job_listing and job_listing.company:
            # Get the company name from the job listing's associated company
            
            company_name = job_listing.company.registered_name
            company_id= job_listing.company.id
            
            # Send the notification with company name
            notify_subscribed_alumnus(f"{company_name} posted a new listing, {job_listing.title}!", company_id)
            
        flash('Job published successfully!', 'success')
        subscribed_alumni = Notification.query.all()
        print(len(subscribed_alumni))
        response = redirect(url_for('index_views.index_page'))
    else:
        flash('Job not found', 'unsuccessful')
        response = redirect(url_for('index_views.index_page'))
    return response


# handle unpublish
@admin_views.route('/unpublish_job/<int:job_id>', methods=['POST'])
@jwt_required()
def unpublish_job(job_id):
    toggled = toggle_listing_approval(job_id,status='PENDING')

    if not toggled:
        flash('Job unpublished successfully!', 'success')
        response = redirect(url_for('index_views.index_page'))
    else:
        flash('Job not found', 'unsuccessful')
        response = (redirect(url_for('index_views.index_page')))

    return response  # Redirect to the admin dashboard

# handle deletion
@admin_views.route('/delete_listing/<int:job_id>', methods=['GET'])
@jwt_required()
def delete_listing_action(job_id):
    listing = get_listing(job_id)
    #store values before listing is deleted
    company_id= listing.company_id
    company_name= listing.company.registered_name
    title= listing.title
   
    deleted = delete_listing(job_id)
  
    if deleted:
        message = f"Ahoy {company_name}! Your listing, {title} has been deleted!"
        notify_company_account(message, company_id)
        flash('Job listing deleted!', 'success')
        response = redirect(url_for('index_views.index_page'))
    else:
        flash('Error deleting job listing', 'unsuccessful')
        response = (redirect(url_for('index_views.index_page')))

    return response

@admin_views.route('/admin_notifications', methods=['GET'])
@jwt_required()
def view_notifications_page():
    
    admin = current_user
    
    if not isinstance(admin, AdminAccount):
        flash('Not an Alumnus', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    try:
        # Fetch notifications for the alumnus
        notifications = admin.notifications.all()
        return render_template('admin_notifications.html', notifications=notifications, admin=current_user)
    
    except Exception as e:
        flash('Error retrieving notifications', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

# @index_views.route('/delete-exercise/<int:exercise_id>', methods=['GET'])
# @login_required
# def delete_exercise_action(exercise_id):
    
#     user = current_user

#     res = delete_exerciseSet(exercise_id)

#     if res == None:
#         flash('Invalid or unauthorized')
#     else:
#         flash('exercise deleted!')
#     return redirect(url_for('user_views.userInfo_page'))


# handle updates
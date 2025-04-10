from flask import Blueprint, flash, redirect, render_template, url_for
from App.models import db

from flask_jwt_extended import jwt_required, current_user

from .index import index_views


from App.controllers import (
    get_company_by_id,
    get_listing,
    delete_listing,
    toggle_listing_approval,
    notify_users
)

from App.models import (
    CompanySubscription,
    AdminAccount
)

admin_views = Blueprint(
    'admin_views',
    __name__,
    template_folder='../templates'
)

# ---------- JOB ACTION ROUTES ----------


@admin_views.route('/publish_job/<int:job_id>', methods=['POST'])
@jwt_required()
def publish_job(job_id):
    """
    Approves a job listing and notifies both the posting company and subscribed alumni.
    """
    listing = toggle_listing_approval(job_id, status='APPROVED')

    if listing and listing.company_id:   
        company = get_company_by_id(listing.company_id)   
        
        if not company:
            flash('Company not found for this listing.', 'unsuccessful')
            return redirect(url_for('index_views.index_page'))

        flash('Job published successfully!', 'success')

        # Notify company
        company_msg = f"You job listing, {listing.title} has been published!"
        notify_users(company_msg, "company", company.id)

        # Notify subscribed alumni
        subscriptions = CompanySubscription.query.filter_by(company_id=company.id).all()
        alumnus_ids = [sub.id for sub in subscriptions if sub.alumnus_id]

        if alumnus_ids:
            subscriber_notification = f"{company.registered_name} posted a new listing, {listing.title}!"
            notify_users(subscriber_notification, "alumni", alumnus_ids)
    else:
        flash('Job not found or could not be published.', 'unsuccessful')

    return redirect(url_for('index_views.index_page'))


@admin_views.route('/unpublish_job/<int:job_id>', methods=['POST'])
@jwt_required()
def unpublish_job(job_id):
    """
    Unpublishes a job listing (sets status to PENDING).
    """
    result = toggle_listing_approval(job_id, status='PENDING')

    if not result:
        flash('Job unpublished successfully!', 'success')
    else:
        flash('Job not found or unpublishing failed.', 'unsuccessful')

    return redirect(url_for('index_views.index_page'))


@admin_views.route('/delete_listing/<int:job_id>', methods=['GET'])
@jwt_required()
def delete_listing_action(job_id):
    """
    Deletes a job listing and notifies the associated company.
    """
    listing = get_listing(job_id)

    if not listing:
        flash('Job listing not found.', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    message = f"Ahoy {listing.company.registered_name}! Your listing, {listing.title}, has been deleted!"

    if delete_listing(job_id):
        notify_users(message, "company", listing.company_id)
        flash('Job listing deleted!', 'success')
    else:
        flash('Error deleting job listing', 'unsuccessful')

    return redirect(url_for('index_views.index_page'))

# ---------- ADMIN NOTIFICATIONS ----------


@admin_views.route('/admin_notifications', methods=['GET'])
@jwt_required()
def view_notifications_page():
    """
    Displays notifications for the currently logged-in admin.
    """
    if not isinstance(current_user, AdminAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

    try:
        notifications = current_user.notifications.all()
        return render_template('admin_notifications.html', notifications=notifications, admin=current_user)

    except Exception as e:
        print(f"[ERROR] Failed to retrieve admin notifications: {e}")
        flash('Error retrieving notifications.', 'unsuccessful')
        return redirect(url_for('index_views.index_page'))

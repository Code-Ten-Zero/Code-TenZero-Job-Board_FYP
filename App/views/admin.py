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

INDEX_PAGE_URL = url_for('index_views.index_page')

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
        return redirect(INDEX_PAGE_URL)
    
    listing = toggle_listing_approval(job_id, status='APPROVED')

    if not listing:
        flash('Job not found or could not be published.', 'unsuccessful')
        return redirect(INDEX_PAGE_URL)

    company = get_company_by_id(listing.company_id)

    # Notify company
    company_msg = f"Your job listing, {listing.title} has been published!"
    notify_users(company_msg, "company", company.id)
    send_job_published_email(company, listing, company, is_company=True)

    # Notify subscribed alumni
    subscribed_alumni = CompanySubscription.query.filter_by(
        company_id=company.id).all()

    if subscribed_alumni:
        subscribed_ids = [sub.id for sub in subscribed_alumni]
        subscriber_notification = f"{company.registered_name} posted a new listing, {listing.title}!"
        notify_users(subscriber_notification, "alumni", subscribed_ids)

        for alumnus in subscribed_alumni:
            send_job_published_email(
                alumnus, listing, company, is_company=False)

    flash('Job published successfully!', 'success')
    return redirect(INDEX_PAGE_URL)


@admin_views.route('/unpublish_job/<int:job_id>', methods=['POST'])
@jwt_required()
def unpublish_job(job_id):
    """
    Sets a job listing's status to "PENDING" and notifies the associated company and subscribed alumni.
    """
    if not isinstance(current_user, AdminAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(INDEX_PAGE_URL)
    
    listing = toggle_listing_approval(job_id, status='PENDING')

    if not listing:
        flash('Job not found or unpublishing failed.', 'unsuccessful')
        return redirect(INDEX_PAGE_URL)

    company = get_company_by_id(listing.company_id)

    # Notify company
    company_msg = f"Your job listing, {listing.title} has been temporarily unpublished!"
    notify_users(company_msg, "company", company.id)
    send_job_published_email(company, listing, company, is_company=True)

    # Notify subscribed alumni
    subscribed_alumni = CompanySubscription.query.filter_by(
        company_id=company.id).all()

    if subscribed_alumni:
        subscribed_ids = [sub.id for sub in subscribed_alumni]
        subscriber_notification = f"The job listing {listing.title} by company {company.registered_name} has been temporarily unpublished."
        notify_users(subscriber_notification, "alumni", subscribed_ids)

        for alumnus in subscribed_alumni:
            send_job_published_email(
                alumnus, listing, company, is_company=False)

    flash('Job unpublished successfully!', 'success')
    return redirect(INDEX_PAGE_URL)


@admin_views.route('/delete_listing/<int:job_id>', methods=['GET'])
@jwt_required()
def delete_listing_action(job_id):
    """
    Deletes a job listing and notifies the associated company and subscribed alumni.
    """
    if not isinstance(current_user, AdminAccount):
        flash('Unauthorized access', 'unsuccessful')
        return redirect(INDEX_PAGE_URL)

    listing = get_listing(job_id)

    if not listing:
        flash('Job listing not found.', 'unsuccessful')
        return redirect(INDEX_PAGE_URL)

    if delete_listing(job_id):
        company = get_company_by_id(listing.company_id)

        # Notify company
        company_msg = f"Your job listing, {listing.title} has been published!"
        notify_users(company_msg, "company", company.id)
        send_job_deleted_email(company, listing, company, is_company=True)

        # Notify subscribed alumni
        subscribed_alumni = CompanySubscription.query.filter_by(
            company_id=company.id).all()

        if subscribed_alumni:
            subscribed_ids = [sub.id for sub in subscribed_alumni]
            subscriber_notification = f"{company.registered_name} posted a new listing, {listing.title}!"
            notify_users(subscriber_notification, "alumni", subscribed_ids)

            for alumnus in subscribed_alumni:
                send_job_deleted_email(
                    alumnus, listing, company, is_company=False)

        flash('Job listing deleted!', 'success')
    else:
        flash('Error deleting job listing', 'unsuccessful')

    return redirect(INDEX_PAGE_URL)


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
        return redirect(INDEX_PAGE_URL)

    try:
        notifications = current_user.notifications.all()
        return render_template('admin_notifications.html', notifications=notifications, admin=current_user)

    except Exception as e:
        print(f"[ERROR] Failed to retrieve admin notifications: {e}")
        flash('Error retrieving notifications.', 'unsuccessful')
        return redirect(INDEX_PAGE_URL)

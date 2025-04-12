from flask import Blueprint, flash, redirect, render_template, url_for
from flask_jwt_extended import current_user, jwt_required

from App.controllers.job_listing import (
    approve_job_listing,
    unapprove_job_listing,
    delete_job_listing
)

from App.controllers.company_account import (
    get_company_account
)

from App.controllers.notifications import (
    notify_subscribed_alumnus
)

from App.models import(
    AdminAccount
)

admin_views = Blueprint(
    'admin_views',
    __name__,
    template_folder='../templates'
)

INDEX_PAGE_URL = 'index_views.index_page'


@admin_views.route('/publish_job/<int:job_listing_id>', methods=['POST'])
@jwt_required()
def publish_job(job_listing_id):
    approved_listing = approve_job_listing(job_listing_id)

    if approved_listing:
        listing_company = get_company_account(approved_listing.company_id)

        if listing_company:
            company_name = listing_company.registered_name
            company_id = listing_company.id

            notify_subscribed_alumnus(
                f"{company_name} posted a new listing, {approved_listing.title}!",
                company_id
            )

        flash('Job published successfully!', 'success')
        response = redirect(url_for(INDEX_PAGE_URL))

    else:
        flash('Job not found', 'unsuccessful')
        response = redirect(url_for(INDEX_PAGE_URL))

    return response


@admin_views.route('/unpublish_job/<int:job_listing_id>', methods=['POST'])
@jwt_required()
def unpublish_job(job_listing_id):
    unpublished_listing = unapprove_job_listing(job_listing_id)

    if not unpublished_listing:
        flash('Job unpublished successfully!', 'success')
        response = redirect(url_for(INDEX_PAGE_URL))
    else:
        flash('Job not found', 'unsuccessful')
        response = (redirect(url_for(INDEX_PAGE_URL)))

    return response


@admin_views.route('/delete_listing/<int:job_listing_id>', methods=['GET'])
@jwt_required()
def delete_listing_action(job_listing_id):

    deleted_listing = delete_job_listing(
        job_listing_id,
        current_user.id
    )

    response = None

    if deleted_listing:
        flash('Job listing deleted!', 'success')
        response = redirect(url_for(INDEX_PAGE_URL))
    else:
        flash('Error deleting job listing', 'unsuccessful')
        response = (redirect(url_for(INDEX_PAGE_URL)))

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
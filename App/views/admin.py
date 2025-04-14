from flask import Blueprint, flash, redirect, render_template, url_for
from flask_jwt_extended import current_user, jwt_required

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
    notify_company_account,
    notify_subscribed_alumni
)


from App.models import AdminAccount

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

    # Notify company
    notify_company_account(
        f"Your job listing, {approved_listing.title} has been published!",
        company.id
    )
    send_job_published_email(company, approved_listing, company)

    # Notify subscribed alumni
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

    # Notify company
    notify_company_account(
        f"Your job listing, {unapproved_listing.title} has been temporarily unpublished!",
        company.id
    )
    send_job_unpublished_email(
        company,
        unapproved_listing,
        company
    )

    # Notify subscribed alumni
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


@admin_views.route('/delete_listing/<int:job_id>', methods=['GET'])
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

    if not delete_job_listing(job_id):
        flash('Error deleting job listing', 'unsuccessful')

    else:
        company = get_company_account(temp_listing_copy.company_id)

        # Notify company
        notify_company_account(
            f"Your job listing, {temp_listing_copy.title} has been deleted!",
            company.id
        )
        send_job_deleted_email(company, temp_listing_copy, company)

        # Notify subscribed alumni
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
        notifications = current_user.notifications.all()
        return render_template('admin_notifications.html', notifications=notifications, admin=current_user)

    except Exception as e:
        print(f"[ERROR] Failed to retrieve admin notifications: {e}")
        flash('Error retrieving notifications.', 'unsuccessful')
        return redirect(url_for(INDEX_PAGE_ROUTE))

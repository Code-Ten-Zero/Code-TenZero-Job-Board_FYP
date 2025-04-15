from flask import Blueprint, redirect, render_template, jsonify, url_for
from App.models import db
from flask_jwt_extended import current_user, jwt_required

from App.controllers import (
    get_all_job_listings,
    get_job_listings_by_company_id,
    add_job_listing,
    add_alumnus_account,
    add_admin_account,
    add_company_account,
    get_approved_listings,
    get_all_company_accounts,
    get_user_by_email
)

from App.controllers.job_applications import (
    get_job_applications_by_alumnus_id
)

from App.controllers.saved_job_listing import (
    get_saved_job_listings_by_alumnus_id
)

from App.models import (
    AlumnusAccount,
    CompanyAccount,
    AdminAccount,
)

index_views = Blueprint(
    'index_views',
    __name__,
    template_folder='../templates'
)


@index_views.route('/app', methods=['GET'])
@jwt_required()
def index_page():
    jobs = get_all_job_listings()
    companies = get_all_company_accounts()
    approved_jobs = get_approved_listings()

    # Use current_user directly if already loaded
    user = current_user

    if isinstance(user, AlumnusAccount):
        saved = get_saved_job_listings_by_alumnus_id(user.id)
        applications = get_job_applications_by_alumnus_id(user.id)

        show_modal = False  # TODO: Replace with `user.has_seen_modal`
        return render_template(
            'alumnus.html',
            jobs=approved_jobs,
            show_modal=show_modal,
            companies=companies,
            user=user,
            saved=saved,
            applications=applications
        )

    if isinstance(user, CompanyAccount):
        company_listings = get_job_listings_by_company_id(user.id)
        return render_template(
            'company-view.html',
            company_listings=company_listings,
            jobs=approved_jobs,
            companies=companies,
            user=user
        )

    if isinstance(user, AdminAccount):
        return render_template('admin.html', jobs=jobs, user=user)

    return redirect(url_for('auth_views.login'))


@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()

    # Add debug records

    # add in the first admin
    add_admin_account('bobpass', 'bob@mail')

    # add in alumni
    add_alumnus_account(
        'robpass',
        'rob@mail',
        'robfname',
        'roblname',
        '1868-333-4444'
    )

    # add in companies
    company1 = add_company_account(
        'company@mail',
        'compass',
        'company1',
        'company_address',
        'public@email',
        'company_website.com',
        'contact'
    )
    company2 = add_company_account(
        'company@mail2',
        'compass',
        'company2',
        'company_address2',
        'public@email2',
        'company_website2.com',
        'contact2',
    )

    # add in job listings
    add_job_listing(
        company1.id,
        'listing1',
        'Full-time',
        'job description1',
        8000,
        True
    )

    add_job_listing(
        company2.id,
        'listing2',
        'Full-time',
        'job description',
        4000,
        True
    )

    return jsonify(message='db initialized!')


@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

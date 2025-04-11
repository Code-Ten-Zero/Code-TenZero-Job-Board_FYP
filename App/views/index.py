import os
from flask import Blueprint, abort, redirect, render_template, request, send_from_directory, jsonify, url_for, flash, send_file
from App.models import db
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from App.controllers import(
    get_job_listing,
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

from App.controllers.saved_job_listing import(
    get_saved_job_listings_by_alumnus_id
)

from App.controllers.job_applications import (
    get_job_applications_by_alumnus_id
)

from App.models import(
    AlumnusAccount,
    CompanyAccount,
    AdminAccount,
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')



# @index_views.route('/', methods=['GET'])
@index_views.route('/app', methods=['GET'])
@jwt_required()
def index_page():
    # return render_template('index.html')
    jobs = get_all_job_listings()
    companies= get_all_company_accounts()
    approved_jobs = get_approved_listings() # retrieve approved jobs
    user= get_user_by_email(current_user.login_email)
    saved_alumni_listings = get_saved_job_listings_by_alumnus_id(user.id)
    alumni_job_applications = get_job_applications_by_alumnus_id(user.id)

    if isinstance(current_user, AlumnusAccount):

        #show_modal = current_user.has_seen_modal
        show_modal = True
        if not show_modal:
            # Pass True to the template to show modal
            return render_template('alumni.html', jobs=approved_jobs, show_modal=True, companies=companies, user=user, saved=saved_alumni_listings, applications= alumni_job_applications)
        
        # Pass False to the modal if already seen
        return render_template('alumni.html', jobs=approved_jobs, show_modal=False, companies=companies, user=user, saved=saved_alumni_listings, applications= alumni_job_applications)

    
    if isinstance(current_user, CompanyAccount):
        company_listings = get_job_listings_by_company_id(current_user.id)
        return render_template('company-view.html', company_listings=company_listings,jobs=approved_jobs, companies=companies)

    if isinstance(current_user, AdminAccount):
        return render_template('admin.html', jobs=jobs)
    
    return redirect('/login')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()

    # add in the first admin
    add_admin_account('bobpass','bob@mail')

    # add in alumni
    add_alumnus_account('robpass','rob@mail', 'robfname', 'roblname', '1868-333-4444')

    # add in companies
    add_company_account('company1', 'compass', 'company@mail',  'company_address', 'contact', 'public@email','company_website.com')
    add_company_account('company2', 'compass', 'company@mail2',  'company_address2', 'contact2', 'public@email2' ,'company_website2.com')
    
    # add in job listings
    add_job_listing('1','listing1', 'Full-time' ,'job description1', 'company1',
                8000, True, 'Curepe')

    add_job_listing('2','listing2', 'job description', 'company2',
                4000, 'Full-time', True, True, 'desiredCandidate?', 'Curepe', ['Database Manager', 'Programming', 'butt'])


    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
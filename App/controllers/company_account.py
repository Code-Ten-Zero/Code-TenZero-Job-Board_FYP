from App.models import BaseUserAccount, CompanyAccount, JobListing, AlumnusAccount, AdminAccount
from App.database import db
from App.controllers import get_all_subscribed_alumni



def add_company(registered_name, password, login_email, mailing_address, phone_number, public_email, website_url):
    # Check if there are no other users with the same username or email values in any other subclass
        if (
            # Company.query.filter_by(email=email).first() is not None or
            AdminAccount.query.filter_by(login_email=login_email).first() is not None or
            AlumnusAccount.query.filter_by(login_email=login_email).first() is not None
            
        ):
            return None  # Return None to indicate duplicates

        newCompany= CompanyAccount(login_email, password,registered_name, mailing_address, public_email, website_url, phone_number,profile_photo_file_path="N/A")
        try: # safetey measure for trying to add duplicate 
            db.session.add(newCompany)
            db.session.commit()  # Commit to save the new  to the database
            return newCompany
        except:
            db.session.rollback()
            return None

def send_notification(job_categories=None):
    # get all the subscribed users who have the job categories
    subbed = get_all_subscribed_alumni()

    # turn the job categories into a set for intersection
    job_categories = set(job_categories)

    # list of alumni to be notified
    notif_alumni = []
    # print(job_categories)

    for alumni in subbed:
        # print('alumni')
        # get a set of all the job categories the alumni is subscribed for
        jobs = set(alumni.get_categories())
        common_jobs = []
        # perform an intersection of the jobs an alumni is subscribed for and the job categories of the listing
        common_jobs = list(jobs.intersection(job_categories))

        # if there are common jobs shared in the intersection, then add that alumni the list to notify
        if common_jobs:
            notif_alumni.append(alumni)
        # else:
        #     print('no commmon jobs: ', alumni, ' and ', job_categories)

    # do notification send here? use mail chimp?
    print(notif_alumni, job_categories)
    return notif_alumni, job_categories

def add_listing(company_id, title, position_type, description,
                monthly_salary_ttd, is_remote, job_site_address, datetime_created, datetime_last_modified, admin_approval_status):

    # manually validate that the company actually exists
    company = get_company_by_id(company_id)
    if not company:
        return None

    newListing = JobListing(company_id, title, position_type, description, 
                monthly_salary_ttd, is_remote, job_site_address, datetime_created, datetime_last_modified, admin_approval_status)
    try:
        db.session.add(newListing)
        db.session.commit()

        # print('get_all_subscribed_alumn')
        # send_notification(job_categories)
        # send_notification(newListing.get_categories())

        # print('yah')
        return newListing
    except:
        # print('nah')
        db.session.rollback()
        return None
    
def get_company_by_id (id):
    return CompanyAccount.query.filter_by(id=id).first()

def get_company_by_email(login_email):
    return CompanyAccount.query.filter_by(login_email=login_email).first()

def get_company_listings(login_email):
    # return Listing.query.filter_by(company_name=company_name)
    company = get_company_by_email(login_email)
    
    if company is None:
        raise ValueError(f"No company found with email: {login_email}")
    
    if not company.job_listings:
        return "No job listings found for this company."
    # for listing in company.listings:
    #     print(listing.get_json())
    return company.job_listings

def get_all_companies():
    return CompanyAccount.query.all()

def get_all_companies_json():
    companies = get_all_companies()
    if not companies:
        return []
    companies = [company.get_json() for company in companies]
    return companies